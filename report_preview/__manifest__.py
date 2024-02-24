# -*- encoding: utf-8 -*-
{
    'name': 'Report Preview',
    'version': '1.0',
    'description': 'Allows to preview a report.',
    'author': 'Jhorel Revilla',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/report_preview_views.xml',
        'views/menu.xml',
        'views/report_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'report_preview/static/src/css/adjust_height.css',
        ],
    },
    'auto_install': False,  
    'application': True
}