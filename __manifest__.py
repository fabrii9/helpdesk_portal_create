# -*- coding: utf-8 -*-
{
    'name': 'Helpdesk Portal - Crear Tickets',
    'version': '1.0',
    'category': 'Services/Helpdesk',
    'summary': 'Permite a los clientes del portal crear tickets de helpdesk',
    'description': """
        Este módulo extiende el portal de Helpdesk para permitir que los 
        usuarios del portal creen nuevos tickets directamente desde su cuenta.
    """,
    'author': 'Custom',
    'depends': ['helpdesk', 'portal'],
    'data': [
        'views/portal_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
