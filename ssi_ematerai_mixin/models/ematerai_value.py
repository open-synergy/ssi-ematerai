# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class EmateraiValue(models.Model):
    _name = "ematerai.value"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "E-Materai Value"

    ematerai_value = fields.Char(
        string="E-Materai Value",
    )
