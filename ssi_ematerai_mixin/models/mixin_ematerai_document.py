# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo import api, fields, models


class MixinEmateraiDocument(models.AbstractModel):
    _name = "mixin.ematerai_document"
    _description = "Mixin for Ematerai Document"

    _ematerai_document_create_page = False
    _ematerai_document_page_xpath = "//page[last()]"
    _ematerai_document_button_xpath = "//header//button[last()]"

    ematerai_document_ids = fields.One2many(
        string="E-Materai Document(s)",
        comodel_name="ematerai.document",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
    )

    @api.multi
    def _action_create_ematerai(self):
        self.ensure_one()
        return True

    @api.multi
    def action_create_ematerai(self):
        for document in self:
            document._action_create_ematerai()

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        if view_type == "form" and self._ematerai_document_create_page:
            doc = etree.XML(res["arch"])
            for node in doc.xpath(self._ematerai_document_page_xpath):
                str_element = self.env["ir.qweb"].render(
                    "ssi_ematerai_mixin.ematerai_document_page"
                )
                new_node = etree.fromstring(str_element)
                node.addnext(new_node)
            for node in doc.xpath(self._ematerai_document_button_xpath):
                str_element = self.env["ir.qweb"].render(
                    "ssi_ematerai_mixin.ematerai_create_button"
                )
                new_node = etree.fromstring(str_element)
                node.addnext(new_node)

            view_model = self.env["ir.ui.view"]
            new_arch, new_fields = view_model.postprocess_and_fields(
                self._name, doc, res["view_id"]
            )
            # raise UserError(_("%s")%(str(view)))
            res["arch"] = new_arch
            new_fields.update(res["fields"])
            res["fields"] = new_fields
        return res
