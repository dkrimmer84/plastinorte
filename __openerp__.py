# -*- coding: utf-8 -*-
{
    'name': "plastinorte",

    'summary': "Plastinorte First Addon Test 23456",

    'description': "Plastinorte First Addon Test",

    'author': "Plastinorte S.A.S",
    'website': "http://www.plastinorte.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Contabilidad',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
}