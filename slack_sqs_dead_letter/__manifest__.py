# -*- coding: utf-8 -*-
{
    'name': 'Slack SQS Dead Letter',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base','slack'],
    'external_dependencies': {
        'python3' : ['boto3'],
    },
    'data': [
        'data/ir_config_parameter.xml',
        'data/ir_cron.xml',
    ],
    'installable': True,
    'auto_install': False,    
}