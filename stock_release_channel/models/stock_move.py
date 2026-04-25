# Copyright 2020 Camptocamp
# Copyright 2022 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def release_available_to_promise(self):
        # after releasing, we re-assign a release channel,
        # as we may release only partially, the channel may
        # change
        res = super().release_available_to_promise()
        # As moves can be merged (and then unlinked), we should ensure
        # they still exist.
        moves = self.exists()
        for picking in moves.picking_id:
            if picking.release_channel_id.recompute_channel_on_pickings_at_release:
                picking.assign_release_channel()
        return res

    def _unreleased_to_backorder(self, split_order=False):
        if split_order:
            self = self.with_context(skip_assign_release_channel=True)
            origin_pickings = self.picking_id
        res = super()._unreleased_to_backorder(split_order=split_order)
        if split_order:
            origin_pickings.filtered(
                lambda p: p.state not in ("draft", "cancel") and p.need_release
            )._delay_assign_release_channel()
        return res

    def _assign_picking_post_process(self, new=False):
        res = super()._assign_picking_post_process(new=new)
        if not self.env.context.get("skip_assign_release_channel"):
            pickings = self.filtered("need_release").picking_id
            if pickings:
                pickings._delay_assign_release_channel()
        return res

    def _release_get_expected_date(self):
        """Return the new scheduled date of a single delivery move"""
        channel = self.picking_id.release_channel_id
        expected_date = channel and channel._get_expected_date()
        if not expected_date:
            return super()._release_get_expected_date()
        return expected_date
