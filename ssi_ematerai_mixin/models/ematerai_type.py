# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EmateraiType(models.Model):
    _name = "ematerai.type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "E-Materai Type"

    model_id = fields.Many2one(
        string="Referenced Model",
        comodel_name="ir.model",
        required=True,
        ondelete="restrict",
    )
    model = fields.Char(
        related="model_id.model",
        index=True,
        store=True,
    )
    api_name = fields.Char(
        string="API Type Name",
        required=True,
    )

    @api.depends(
        "model_id",
        "model",
    )
    def _compute_allowed_report_ids(self):
        obj_ir_actions_report = self.env["ir.actions.report"]

        for document in self:
            result = []
            criteria = [("model", "=", document.model)]
            report_ids = obj_ir_actions_report.search(criteria)
            if report_ids:
                result = report_ids.ids
            document.allowed_report_ids = result

    allowed_report_ids = fields.Many2many(
        string="Allowed Reports",
        comodel_name="ir.actions.report",
        compute="_compute_allowed_report_ids",
        store=False,
    )
    report_id = fields.Many2one(
        string="Report",
        comodel_name="ir.actions.report",
        required=True,
        ondelete="restrict",
    )
    certificate_level = fields.Selection(
        string="Certificate Level",
        selection=[
            ("not_certified", "NOT_CERTIFIED"),
            ("no_changes_allowed", "NO_CHANGES_ALLOWED"),
        ],
        default="not_certified",
    )
    visual_iix = fields.Float(
        string="Left Horizontal",
        default="12.0",
    )
    visual_iiy = fields.Float(
        string="Left Vertical",
        default="22.0",
    )
    visual_urx = fields.Float(
        string="Right Horizontal",
        default="32.0",
    )
    visual_ury = fields.Float(
        string="Right Vertical",
        default="42.0",
    )
    value_id = fields.Many2one(
        string="E-Materai Value",
        comodel_name="ematerai.value",
        required=True,
        ondelete="restrict",
    )
    param_id = fields.Many2one(
        string="E-Materai Parameter",
        comodel_name="ematerai.param",
    )
    visual_sign_page = fields.Integer(string="Stamping Page Number", default="1")

    @api.constrains(
        "visual_sign_page",
    )
    def _check_visual_sign_page(self):
        str_error = _("Stamping cannot be done on the page 0")
        for document in self:
            if document.visual_sign_page == 0:
                raise UserError(str_error)
