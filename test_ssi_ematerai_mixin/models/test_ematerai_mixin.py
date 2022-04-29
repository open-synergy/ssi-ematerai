# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class TestEmaterai(models.Model):
    _name = "test.ematerai"
    _description = "Test Ematerai"
    _inherit = [
        "mixin.ematerai_document",
        "mail.thread",
    ]
    _ematerai_document_create_page = True

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    user_id = fields.Many2one(
        string="User",
        comodel_name="res.users",
    )
    date = fields.Date(
        string="Date",
        index=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=False,
        default=fields.Date.context_today,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    notes = fields.Text(
        string="Notes",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "On Progress"),
            ("done", "Finished"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
    )

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
        }

    @api.multi
    def action_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())

    @api.multi
    def _prepare_open_data(self):
        self.ensure_one()
        return {
            "state": "open",
        }

    @api.multi
    def action_open(self):
        for document in self:
            document.write(document._prepare_open_data())

    @api.multi
    def _prepare_done_data(self):
        self.ensure_one()
        return {
            "state": "done",
        }

    @api.multi
    def action_done(self):
        for document in self:
            document.write(document._prepare_done_data())

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
        }

    @api.multi
    def action_cancel(self):
        for document in self:
            document.write(document._prepare_cancel_data())

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
        }

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())
