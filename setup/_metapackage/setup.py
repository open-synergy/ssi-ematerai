import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-open-synergy-ssi-ematerai",
    description="Meta package for open-synergy-ssi-ematerai Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-ssi_ematerai_mixin',
        'odoo11-addon-ssi_ematerai_redphoenix',
        'odoo11-addon-test_ssi_ematerai_mixin',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 11.0',
    ]
)
