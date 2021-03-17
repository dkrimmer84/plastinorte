
{
    'name': 'Plastinorte',
    'category': 'Localization',
    'version': '12.0.0.1.0',
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
	    'fleet',
        'sale'
    ],
    'installable': True,
    'data': [
        'views/product.xml',
        'wizard/pos_box.xml',
        'views/category.xml',
        'views/register_expense.xml',
        'views/scripts.xml',
	    'views/fleet.xml',
	    'views/report_deliveryslip.xml',
	    'views/report_saleorder.xml',
        'views/report_purchaseorder.xml',
        'views/report_quotationrequest.xml',
        'views/point_of_sale.xml',
        'views/account_payment_term.xml'
    ],
    'qweb': [
        "static/src/xml/inherit.xml",
    ],
}
