# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class EmateraiParam(models.Model):
    _name = "ematerai.param"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "E-Materai Parameter"

    ematerai_param_ids = fields.One2many(
        string="Paremeters",
        comodel_name="ematerai.param_detail",
        inverse_name="param_id",
    )
