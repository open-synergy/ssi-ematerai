# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "E-Materai Redphoenix",
    "version": "11.0.1.2.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_ematerai_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ematerai_provider_data.xml",
        "data/ir_config_parameter.xml",
        "data/ematerai_parameter_data.xml",
        "views/ematerai_redphoenix_views.xml",
        "views/res_config_settings_views.xml",
    ],
}
