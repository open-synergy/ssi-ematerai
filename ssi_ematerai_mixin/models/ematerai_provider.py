# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class EmateraiProvider(models.Model):
    _name = "ematerai.provider"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "E-Materai Provider"

    model_name = fields.Char(string="Provider Model Name")
