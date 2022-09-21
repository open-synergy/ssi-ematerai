# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class EmateraiDocument(models.Model):
    _name = "ematerai.document"
    _description = "E-Materai Document"

    model = fields.Char(
        string="Related Document Model",
        index=True,
    )
    res_id = fields.Integer(
        string="Related Document ID",
        index=True,
    )
    stamping_order = fields.Char(
        string="Stamping Order ID",
        index=True,
    )
    original_attachment_id = fields.Many2one(
        string="Attachment(Original)",
        comodel_name="ir.attachment",
    )
    original_attachment_data = fields.Binary(
        string="File Content Attachment(Original)",
        related="original_attachment_id.datas",
        store=False,
    )
    original_datas_fname = fields.Char(
        string="Filename Attachment(Original)",
        related="original_attachment_id.datas_fname",
        store=False,
    )
    ematerai_attachment_id = fields.Many2one(
        string="Attachment(E-Materai)",
        comodel_name="ir.attachment",
    )
    ematerai_attachment_data = fields.Binary(
        string="File Content Attachment(E-Materai)",
        related="ematerai_attachment_id.datas",
        store=False,
    )
    ematerai_datas_fname = fields.Char(
        string="Filename Attachment(E-Materai)",
        related="ematerai_attachment_id.datas_fname",
        store=False,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="ematerai.type",
    )
    value_id = fields.Many2one(
        string="Value",
        comodel_name="ematerai.value",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("added", "Document Added"),
            ("updated", "Update Param"),
            ("preparing", "Create Order"),
            ("submitted", "Document Submitted"),
            ("sn_generated", "SN Generated"),
            ("terra_completed", "Terra Completed"),
            ("success", "Success"),
        ],
        default="draft",
    )

    @api.model
    def _selection_provider_id(self):
        result = []
        for model in self.env["ir.model"].sudo().search([]):
            result.append((model.model, model.name))
        return result

    @api.depends(
        "provider_res_id",
        "provider_model_name",
    )
    def _compute_provider_id(self):
        for record in self:
            provider_id = (
                self.env[record.provider_model_name]
                .search(
                    [
                        ("id", "=", record.provider_res_id),
                    ]
                )
                .id
            )
            if not provider_id:
                record.provider_id = None
            else:
                record.provider_id = "{},{}".format(
                    record.provider_model_name,
                    provider_id,
                )

    provider_res_id = fields.Integer(
        string="Provider Res ID",
        index=True,
    )
    provider_model_name = fields.Char(
        string="Provider Model Name",
    )
    provider_id = fields.Reference(
        string="Provider",
        selection=lambda r: r._selection_provider_id(),
        compute="_compute_provider_id",
    )

    @api.multi
    def _action_add_document(self):
        self.ensure_one()
        return True

    @api.multi
    def action_add_document(self):
        for document in self:
            if document.provider_id:
                document.provider_id._action_add_document()

    @api.multi
    def _action_create_order(self):
        self.ensure_one()
        return True

    @api.multi
    def action_create_order(self):
        for document in self:
            if document.provider_id:
                document.provider_id._action_create_order()

    @api.multi
    def _action_update_param(self):
        self.ensure_one()
        return True

    @api.multi
    def action_update_param(self):
        for document in self:
            if document.provider_id:
                document.provider_id._action_update_param()

    @api.multi
    def _action_submit_document(self):
        self.ensure_one()
        return True

    @api.multi
    def action_submit_document(self):
        for document in self:
            if document.provider_id:
                document.provider_id._action_submit_document()

    @api.multi
    def _action_generate_sn(self):
        self.ensure_one()
        return True

    @api.multi
    def action_generate_sn(self):
        for document in self:
            if document.provider_id:
                document.provider_id._action_generate_sn()

    @api.multi
    def _action_complete_tera(self):
        self.ensure_one()
        return True

    @api.multi
    def action_complete_tera(self):
        for document in self:
            if document.provider_id:
                document.provider_id._action_complete_tera()

    @api.multi
    def _action_generate_ematerai(self):
        self.ensure_one()
        return True

    @api.multi
    def action_generate_ematerai(self):
        for document in self:
            if document.provider_id:
                document.provider_id._action_generate_ematerai()

    @api.onchange(
        "type_id",
    )
    def onchange_value_id(self):
        self.value_id = False
        if self.type_id:
            self.value_id = self.type_id.value_id
