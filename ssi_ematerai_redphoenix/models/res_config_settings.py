# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).


from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_redphoenix = fields.Boolean(
        string="Redphoenix",
        default="True",
    )
    rp_client_id = fields.Char(
        string="Client ID",
    )
    rp_client_secret = fields.Char(
        string="Client Secret",
    )
    rp_token = fields.Char(
        string="Static JWT Token",
    )
    rp_token_expiry = fields.Datetime(
        string="Access Token Expire",
    )
    rp_login = fields.Char(
        string="Login API",
    )
    rp_add_document = fields.Char(
        string="Add Doc. API",
    )
    rp_create_order = fields.Char(
        string="Create Order API",
    )
    rp_update_param = fields.Char(
        string="Update Param API",
    )
    rp_submit_document = fields.Char(
        string="Submit Doc. API",
    )
    rp_generate_sn = fields.Char(
        string="Generate SN. API",
    )
    rp_complete_terra = fields.Char(
        string="Complete Terra API",
    )
    rp_download_doc = fields.Char(
        string="Download Doc. API",
    )

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        obj_ir_config_parameter = self.env["ir.config_parameter"].sudo()
        obj_ir_config_parameter.set_param(
            "redphoenix.module_redphoenix", self[0].module_redphoenix
        )
        obj_ir_config_parameter.set_param(
            "redphoenix.rp_client_id", self[0].rp_client_id
        )
        obj_ir_config_parameter.set_param(
            "redphoenix.rp_client_secret", self[0].rp_client_secret
        )
        obj_ir_config_parameter.set_param("redphoenix.rp_token", self[0].rp_token)
        obj_ir_config_parameter.set_param(
            "redphoenix.rp_token_expiry", self[0].rp_token_expiry
        )
        obj_ir_config_parameter.set_param("redphoenix.rp_login", self[0].rp_login)
        obj_ir_config_parameter.set_param(
            "redphoenix.rp_add_document", self[0].rp_add_document
        )
        obj_ir_config_parameter.set_param(
            "redphoenix.rp_create_order", self[0].rp_create_order
        )
        obj_ir_config_parameter.set_param(
            "redphoenix.rp_update_param", self[0].rp_update_param
        )
        obj_ir_config_parameter.set_param(
            "redphoenix.rp_submit_document", self[0].rp_submit_document
        )
        obj_ir_config_parameter.set_param(
            "redphoenix.rp_generate_sn", self[0].rp_generate_sn
        )
        obj_ir_config_parameter.set_param(
            "redphoenix.rp_complete_terra", self[0].rp_complete_terra
        )
        obj_ir_config_parameter.set_param(
            "redphoenix.rp_download_doc", self[0].rp_download_doc
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        obj_ir_config_parameter = self.env["ir.config_parameter"].sudo()
        res.update(
            module_redphoenix=obj_ir_config_parameter.get_param(
                "redphoenix.module_redphoenix", default=False
            ),
            rp_client_id=obj_ir_config_parameter.get_param(
                "redphoenix.rp_client_id", default=False
            ),
            rp_client_secret=obj_ir_config_parameter.get_param(
                "redphoenix.rp_client_secret", default=False
            ),
            rp_login=obj_ir_config_parameter.get_param(
                "redphoenix.rp_login", default=False
            ),
            rp_token=obj_ir_config_parameter.get_param(
                "redphoenix.rp_token", default=False
            ),
            rp_token_expiry=obj_ir_config_parameter.get_param(
                "redphoenix.rp_token_expiry", default=False
            ),
            rp_add_document=obj_ir_config_parameter.get_param(
                "redphoenix.rp_add_document", default=False
            ),
            rp_create_order=obj_ir_config_parameter.get_param(
                "redphoenix.rp_create_order", default=False
            ),
            rp_update_param=obj_ir_config_parameter.get_param(
                "redphoenix.rp_update_param", default=False
            ),
            rp_submit_document=obj_ir_config_parameter.get_param(
                "redphoenix.rp_submit_document", default=False
            ),
            rp_generate_sn=obj_ir_config_parameter.get_param(
                "redphoenix.rp_generate_sn", default=False
            ),
            rp_complete_terra=obj_ir_config_parameter.get_param(
                "redphoenix.rp_complete_terra", default=False
            ),
            rp_download_doc=obj_ir_config_parameter.get_param(
                "redphoenix.rp_download_doc", default=False
            ),
        )
        return res
