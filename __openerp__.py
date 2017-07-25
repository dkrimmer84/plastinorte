# -*- coding: utf-8 -*-

{
    'name': 'Plastinorte',
    'category': 'Localization',
    'version': '9.0.0.1.0',
    'author': 'Dominic Krimmer, Plastinorte S.A.S',
    'license': 'AGPL-3',
    'maintainer': 'dominic.krimmer@gmail.com',
    'website': 'https://www.plastinorte.com',
    'summary': 'Changes made for Plastinorte S.A.S ',
    'depends': [
        'point_of_sale',
        'stock',
        'account',
        'hr_expense',
        'hr',
	'fleet'
    ],
    'installable': True,
    'data': [
        'views/product.xml',
        'wizard/pos_box.xml',
        'views/category.xml',
        'views/register_expense.xml',
<<<<<<< HEAD
        'views/scripts.xml',
	    'views/fleet.xml',
	'views/report_deliveryslip.xml',
	'views/report_saleorder.xml'
    ],
    'qweb': [
        "static/src/xml/inherit.xml",
=======
        'views/point_of_sale.xml',

	'views/fleet.xml'
>>>>>>> master
    ],
}
