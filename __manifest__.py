{
    'name': 'Session Wise Discount Limit',
    'version': '1.0',
    'summary': 'Limits the discount to a specific amount',
    'author': 'Hafsana CA',
    'depends': ['base','point_of_sale'],
    'data': [
            'views/res_config_settings_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_discount_limit/static/src/js/discount_limit.js',
        ],
    },
    'installable': True,
    'application': False,
}