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
                "portal"
                ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/procurement_version.xml',
        'views/procurement_plan.xml',
        'views/work_plan.xml',
        'views/purchase_requisition.xml',
        'portal_views/website_menu.xml',
        'views/tenders_views.xml',
        'portal_views/application_form_template.xml',
        'views/evaluation_criteria_template.xml',
        'portal_views/tender_portal.xml',
        'portal_views/portal_home.xml',
        'portal_views/tender_detail_view.xml',
        'portal_views/custom_signup_view.xml',
    ],
    'js': [
            'static/src/js/website_tender_detail.js',  # Include your JS file here
            'static/src/js/portal_check_logged_in.js',  # Include your JS file here
        ],
    'installable': True,
    'auto_install': False,

}
