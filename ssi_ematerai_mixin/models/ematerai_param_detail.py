# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class EmateraiParamDetail(models.Model):
    _name = "ematerai.param_detail"
    _description = "E-Materai Parameter Detail"

    param_id = fields.Many2one(
        string="E-Materai Parameter",
        comodel_name="ematerai.param",
        required=True,
        ondelete="restrict",
    )
    name = fields.Char(
        string="Name",
    )
    python_code = fields.Text(
        string="Python Code",
        default="""# Available locals:\n#  - rec: current record\n result = []""",
    )
