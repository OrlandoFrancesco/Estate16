{
    'name': "ESTATE",
    'version': '16.1',
    'depends': ['base'],
    'author': "Francesco",
    'description': """
    Modulo ESTATE odoo16
    """,
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_menus.xml',
        'views/res_users.xml',
        'report/estate_property_reports.xml',
        'report/res_user_reports.xml',
        'data/estate_demo.xml'
    ],
    'application': True,
}