{
    'name': "Custom Procurement Plans",

    'summary': """
        Custom Procurement Plans""",

    'description': """
        Custom Procurement Plans
    """,

    'author': "Loomoni Morwo",
    'website': "http://www.loomoni.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'procurement',
    'version': '1.0',
    # any module necessary for this one to work correctly
    'depends': ['base',
                "mail",
                "purchase",
                "hr",
                "stock",
                "website",
                ],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/procurement_version.xml',
        'views/procurement_plan.xml',
        'views/work_plan.xml',
        'views/purchase_requisition.xml',
        'views/website_menu.xml',
        'views/tenders_views.xml',
        'views/website_template.xml',
        'views/tender_detail_view.xml',
    ],
    'js': [
            'static/src/js/website_tender_detail.js',  # Include your JS file here
        ],
    'installable': True,
    'auto_install': False,

}
