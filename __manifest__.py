# -*- coding: utf-8 -*-
{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Real Estate Management',
    'description': """
        Real Estate Management module
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        # 'views/test_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_type.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}