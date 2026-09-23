{
    'name': 'Inventory Dispatch Report',
    'version': '19.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Dispatch report showing demand, delivered and pending quantities across all stock moves',
    'depends': ['base', 'product', 'sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/dispatch_report_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}