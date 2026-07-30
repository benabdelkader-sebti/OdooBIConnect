{
    "name": "OdooBIConnect",
    "version": "15.0.5.0.0",
    'category': 'Tools',
    'summary': 'Odoo Power BI Connect Pro',
    'description': """
        Connect Odoo to Power BI Desktop seamlessly using OData Feed.
        - Secure Authentication via JWT (JSON Web Tokens).
        - No SQL port opening required (Uses HTTPS/8069).
        - Multi-company and Multi-database support.
        - Compatible with Odoo 12, 13, 14, 15, 16, and 17+.
    """,
    "author": "benabdelkader sebti",
    "depends": ["base", "web"],
    "data": [
        "views/config_settings_views.xml",
        "data/ir_config_data.xml",
    ],
    'assets': {
    'web.assets_backend': [
        'odoobiconnect/static/src/js/powerbi_connector.js',
        'odoobiconnect/static/src/js/powerbi_clipboard.js',
    ],
    },
    'images': ['static/description/banner.png'],
    'price': 20.00,
    'currency': 'EUR',
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
