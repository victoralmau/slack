# -*- coding: utf-8 -*-
{
    'name': 'Slack Shipping Expedition',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'shipping_expedition', 'slack'],
    'data': [
        'views/res_users.xml',
    ],    
    'installable': True,
    'auto_install': False,    
}