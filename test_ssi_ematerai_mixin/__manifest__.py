# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Test Module: Ematerai Mixin",
    "version": "11.0.1.0.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mail",
        "ssi_ematerai_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/test_ematerai_mixin_view.xml",
    ],
}
