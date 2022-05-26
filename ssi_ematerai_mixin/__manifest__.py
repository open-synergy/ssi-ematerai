# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "E-Materai Mixin",
    "version": "11.0.1.0.1",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "base",
        "ssi_master_data_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "data/ematerai_value_data.xml",
        "wizards/create_ematerai_views.xml",
        "templates/ematerai_document_templates.xml",
        "views/ematerai_value_views.xml",
        "views/ematerai_provider_views.xml",
        "views/ematerai_type_views.xml",
        "views/ematerai_document_views.xml",
        "views/ematerai_param_views.xml",
    ],
}
