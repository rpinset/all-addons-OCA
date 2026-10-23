# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, api, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


def _exact_ilike(value):
    """A pattern for ``=ilike`` that matches ``value`` exactly, in any case:
    ``%`` and ``_`` are wildcards there, so they are escaped."""
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


class StockScrap(models.Model):
    _inherit = "stock.scrap"

    @api.model
    def _barcode_scrap_location(self, location_id):
        location = self.env["stock.location"].browse(location_id).exists()
        if not location or location.usage != "internal":
            raise UserError(self.env._("The selected location is no longer valid."))
        return location

    @api.model
    def _barcode_scrap_destinations(self, company):
        """The locations a scrap of ``company`` may send its goods to.

        Exactly what the back office's Scrap Location field offers: its domain
        (locations flagged as scrap locations) plus the company check Odoo adds
        to it -- the company's own locations and the shared ones.
        """
        Location = self.env["stock.location"]
        return Location.search(
            [("scrap_location", "=", True)] + Location._check_company_domain(company)
        )

    @api.model
    def _barcode_scrap_default_destination(self, company, location, destinations):
        """Where a scrap of ``company`` goes when the operator picks nothing.

        The back office preselects one of the company's own scrap locations.
        When it has none, the first of the allowed ones (a shared scrap location,
        say) is taken, so a destination that can be offered is never left empty.
        """
        default = self.new(
            {"company_id": company.id, "location_id": location.id}
        ).scrap_location_id
        return (default & destinations) or destinations[:1]

    @api.model
    def _barcode_scrap_available_qty(self, product, lot, location):
        """What a scrap made by the scanner can take of ``product`` and ``lot``.

        The scanner sets neither a package nor an owner on its scraps, so this
        counts what ``check_available_qty`` counts for them: the net quantity at
        the location itself (negative quants included) outside packages and not
        owned by a partner.
        """
        return product.with_context(
            location=location.id,
            lot_id=lot.id,
            package_id=False,
            owner_id=False,
            strict=True,
        ).qty_available

    @api.model
    def action_barcode_scrap_create_reason(self, name):
        """Create a scrap reason from the scanner, as the back office's reason
        field quick-creates one from a typed name.

        A reason that already exists under the same name, whatever its case, is
        returned instead of creating a near-duplicate operators would then have
        to tell apart.
        """
        name = " ".join((name or "").split())
        if not name:
            raise UserError(self.env._("Type a name for the scrap reason."))
        Tag = self.env["stock.scrap.reason.tag"]
        tag = Tag.search(
            [("name", "=ilike", _exact_ilike(name))], limit=1
        ) or Tag.create({"name": name})
        return {"id": tag.id, "name": tag.name}

    @api.model
    def action_barcode_scrap_location_stock(self, location_id):
        """Return what a location holds that a scrap can take, per product and
        lot: one entry each.

        The scanner shows it next to each line (how much there is to scrap) and
        offers only the lots actually stored there. It counts what validating
        the scrap counts (see ``_barcode_scrap_available_qty``): the net
        quantity at the location itself, outside packages and not owned by a
        partner, so the screen and the validation never disagree.
        """
        location = self._barcode_scrap_location(location_id)
        groups = self.env["stock.quant"]._read_group(
            [
                ("location_id", "=", location.id),
                ("package_id", "=", False),
                ("owner_id", "=", False),
            ],
            ["product_id", "lot_id"],
            ["quantity:sum"],
        )
        company = location.company_id or self.env.company
        scrap_locations = self._barcode_scrap_destinations(company)
        default = self._barcode_scrap_default_destination(
            company, location, scrap_locations
        )
        return {
            "location_id": location.id,
            "location_name": location.display_name,
            "scrap_location_id": default.id or False,
            "scrap_locations": [
                {"id": loc.id, "name": loc.display_name} for loc in scrap_locations
            ],
            "stock": [
                {
                    "product_id": product.id,
                    "lot_id": lot.id or False,
                    "lot_name": lot.name or False,
                    "quantity": quantity,
                }
                for product, lot, quantity in groups
                if float_compare(
                    quantity, 0, precision_rounding=product.uom_id.rounding
                )
                > 0
            ],
        }

    @api.model
    def _barcode_scrap_resolve_lot(self, product, line, location):
        """Find the lot/serial a scanned line names.

        The line carries either the id of a lot picked among the location's
        stock or a lot name read from a GS1 label or typed in. A scrap only makes
        sense for a lot that exists, so an unknown name is refused instead of
        creating a new lot.

        The name is matched exactly first: lots that differ only in case are
        distinct lots. Failing that, a name typed in another case finds its lot,
        but only when it names a single one.
        """
        Lot = self.env["stock.lot"]
        if line.get("lot_id"):
            lot = Lot.browse(line["lot_id"]).exists()
            if lot and lot.product_id == product:
                return lot
            raise UserError(
                self.env._(
                    "The lot/serial number chosen for %(name)s is no longer valid.",
                    name=product.display_name,
                )
            )
        lot_name = (line.get("lot_name") or "").strip()
        if not lot_name:
            return Lot
        company = product.company_id or location.company_id or self.env.company
        domain = [
            ("product_id", "=", product.id),
            ("company_id", "in", [company.id, False]),
        ]
        lot = Lot.search(domain + [("name", "=", lot_name)], limit=1)
        if not lot:
            lot = Lot.search(
                domain + [("name", "=ilike", _exact_ilike(lot_name))], limit=2
            )
        if len(lot) > 1:
            raise UserError(
                self.env._(
                    "Several lots/serial numbers of %(name)s match %(lot)s: type "
                    "it exactly as it is written.",
                    lot=lot_name,
                    name=product.display_name,
                )
            )
        if not lot:
            raise UserError(
                self.env._(
                    "There is no lot/serial number %(lot)s for %(name)s.",
                    lot=lot_name,
                    name=product.display_name,
                )
            )
        return lot

    @api.model
    def _barcode_scrap_prepare_lines(self, lines, location):
        """Validate the scanned lines and resolve their products and lots.

        Returns a list of ``(product, lot, qty)`` tuples, the quantity in the
        product's unit of measure. Lines naming the same product and lot are
        merged into one, so the availability check sees the whole quantity
        asked for that stock. Raises a ``UserError`` the scanner shows to the
        operator when a line cannot be scrapped as it stands.
        """
        merged = {}
        for line in lines or []:
            product = (
                self.env["product.product"].browse(line.get("product_id")).exists()
            )
            if not product:
                raise UserError(
                    self.env._("One of the scanned products no longer exists.")
                )
            if product.type != "consu":
                # What the back office's product field offers on a scrap: a service
                # or a combo has no stock to write off.
                raise UserError(
                    self.env._(
                        "%(name)s is not a goods product and cannot be scrapped.",
                        name=product.display_name,
                    )
                )
            qty = float(line.get("qty") or 0)
            if float_compare(qty, 0, precision_rounding=product.uom_id.rounding) <= 0:
                raise UserError(
                    self.env._(
                        "The quantity to scrap for %(name)s must be positive.",
                        name=product.display_name,
                    )
                )
            lot = self.env["stock.lot"]
            if product.tracking != "none":
                lot = self._barcode_scrap_resolve_lot(product, line, location)
                if not lot:
                    raise UserError(
                        self.env._(
                            "Product %(name)s is tracked: scan or choose its "
                            "lot/serial number before scrapping it.",
                            name=product.display_name,
                        )
                    )
            key = (product.id, lot.id)
            if key in merged:
                merged[key][2] += qty
            else:
                merged[key] = [product, lot, qty]
        if not merged:
            raise UserError(self.env._("Scan at least one product to scrap."))
        for product, lot, qty in merged.values():
            if (
                product.tracking == "serial"
                and float_compare(qty, 1, precision_rounding=product.uom_id.rounding)
                != 0
            ):
                raise UserError(
                    self.env._(
                        "Serial number %(lot)s of %(name)s can only be scrapped "
                        "once, one unit.",
                        lot=lot.name,
                        name=product.display_name,
                    )
                )
        return [tuple(entry) for entry in merged.values()]

    @api.model
    def action_barcode_scrap(
        self,
        location_id,
        lines,
        reason_tag_ids=None,
        force=False,
        scrap_location_id=None,
    ):
        """Scrap the scanned lines from one location and validate them at once.

        One ``stock.scrap`` is created per line, carrying the chosen scrap
        reasons, and validated on the spot.

        When a line asks for more than the location holds, nothing is written
        unless ``force`` is set: the lines short of stock are returned so the
        scanner can ask the operator to confirm. That is the choice the back
        office offers through its insufficient-quantity wizard, and confirming
        does what that wizard does -- the scrap is done regardless.

        ``scrap_location_id`` is where the goods go; it must be a scrap location
        of the company. Left empty, the scrap gets the company's default one, as
        in the back office, or the first allowed one when the company has none
        of its own.
        """
        location = self._barcode_scrap_location(location_id)
        prepared = self._barcode_scrap_prepare_lines(lines, location)
        reasons = (
            self.env["stock.scrap.reason.tag"].browse(reason_tag_ids or []).exists()
        )
        company = location.company_id or self.env.company
        destinations = self._barcode_scrap_destinations(company)
        if scrap_location_id:
            scrap_location = self.env["stock.location"].browse(scrap_location_id)
            if scrap_location not in destinations:
                raise UserError(self.env._("The selected scrap location is not valid."))
        else:
            scrap_location = self._barcode_scrap_default_destination(
                company, location, destinations
            )
        if not scrap_location:
            raise UserError(
                self.env._(
                    "There is no scrap location for %(company)s: create one first.",
                    company=company.display_name,
                )
            )
        vals_list = [
            {
                "product_id": product.id,
                "product_uom_id": product.uom_id.id,
                "scrap_qty": qty,
                "lot_id": lot.id,
                "location_id": location.id,
                "company_id": company.id,
                "scrap_reason_tag_ids": [Command.set(reasons.ids)],
                "scrap_location_id": scrap_location.id,
            }
            for product, lot, qty in prepared
        ]

        if not force:
            insufficient = []
            for vals, (product, lot, qty) in zip(vals_list, prepared, strict=True):
                # A virtual scrap runs the very same availability check that
                # validating a real one does, without writing anything.
                if self.new(vals).check_available_qty():
                    continue
                available = self._barcode_scrap_available_qty(product, lot, location)
                insufficient.append(
                    {
                        "product_name": product.display_name,
                        "lot_name": lot.name or False,
                        "requested": qty,
                        "available": available,
                        "uom": product.uom_id.name,
                    }
                )
            if insufficient:
                return {"done": False, "insufficient": insufficient}

        scraps = self.create(vals_list)
        for scrap in scraps:
            if force and not scrap.check_available_qty():
                # The operator confirmed scrapping more than the location holds,
                # which is what the insufficient-quantity wizard does.
                scrap.do_scrap()
                continue
            if isinstance(scrap.action_validate(), dict):
                # The stock moved after it was checked: never scrap more than
                # there is without the operator confirming it.
                raise UserError(
                    self.env._(
                        "The stock of %(name)s changed while scrapping. "
                        "Please try again.",
                        name=scrap.product_id.display_name,
                    )
                )
        return {
            "done": True,
            "count": len(scraps),
            "names": scraps.mapped("name"),
        }
