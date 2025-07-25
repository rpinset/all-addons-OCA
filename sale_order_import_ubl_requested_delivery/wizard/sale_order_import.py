# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import models


class SaleOrderImport(models.TransientModel):
    _inherit = "sale.order.import"

    def _prepare_order(self, parsed_order, price_source):
        res = super()._prepare_order(parsed_order, price_source)
        res["requested_delivery_period_start"] = parsed_order.get(
            "requested_delivery_period_start"
        )
        res["requested_delivery_period_end"] = parsed_order.get(
            "requested_delivery_period_end"
        )
        return res

    def parse_ubl_sale_order(self, xml_root):
        res = super().parse_ubl_sale_order(xml_root)
        ns = xml_root.nsmap
        main_xmlns = ns.pop(None)
        ns["main"] = main_xmlns
        if "RequestForQuotation" in main_xmlns:
            root_name = "main:RequestForQuotation"
        elif "Order" in main_xmlns:
            root_name = "main:Order"
        requested_delivery_xpath = xml_root.xpath(
            f"/{root_name}/cac:Delivery/cac:RequestedDeliveryPeriod", namespaces=ns
        )
        if requested_delivery_xpath:
            if requested_delivery_xpath[0].xpath("cbc:StartDate", namespaces=ns):
                res["requested_delivery_period_start"] = (
                    requested_delivery_xpath[0]
                    .xpath("cbc:StartDate", namespaces=ns)[0]
                    .text
                )
                if requested_delivery_xpath[0].xpath("cbc:StartTime", namespaces=ns):
                    # Remove time zone suffix. Example: 09:30:47.0Z
                    start_time = (
                        requested_delivery_xpath[0]
                        .xpath("cbc:StartTime", namespaces=ns)[0]
                        .text[:8]
                    )
                    res["requested_delivery_period_start"] = (
                        f"{res['requested_delivery_period_start']} {start_time}"
                    )
            if requested_delivery_xpath[0].xpath("cbc:EndDate", namespaces=ns):
                res["requested_delivery_period_end"] = (
                    requested_delivery_xpath[0]
                    .xpath("cbc:EndDate", namespaces=ns)[0]
                    .text
                )
                if requested_delivery_xpath[0].xpath("cbc:EndTime", namespaces=ns):
                    # Remove time zone suffix. Example: 09:30:47.0Z
                    end_time = (
                        requested_delivery_xpath[0]
                        .xpath("cbc:EndTime", namespaces=ns)[0]
                        .text[:8]
                    )
                    res["requested_delivery_period_end"] = (
                        f"{res['requested_delivery_period_end']} {end_time}"
                    )
        return res

    def parse_ubl_sale_order_line(self, line, ns):
        vals = super().parse_ubl_sale_order_line(line, ns)
        line_item = line.xpath("cac:LineItem", namespaces=ns)[0]
        expected_delivery_period = line_item.xpath(
            "cac:Delivery/cac:RequestedDeliveryPeriod", namespaces=ns
        )
        if expected_delivery_period:
            start_date = expected_delivery_period[0].xpath(
                "cbc:StartDate", namespaces=ns
            )
            start_time = expected_delivery_period[0].xpath(
                "cbc:StartTime", namespaces=ns
            )
            end_date = expected_delivery_period[0].xpath("cbc:EndDate", namespaces=ns)
            end_time = expected_delivery_period[0].xpath("cbc:EndTime", namespaces=ns)

            if start_date and end_date:
                if start_time and end_time:
                    start_date = f"{start_date[0].text} {start_time[0].text[:8]}"
                    end_date = f"{end_date[0].text} {end_time[0].text[:8]}"
                else:
                    start_date = start_date[0].text
                    end_date = end_date[0].text

                vals["requested_delivery_period_start"] = start_date
                vals["requested_delivery_period_end"] = end_date
        return vals
