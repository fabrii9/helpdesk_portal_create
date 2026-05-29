# -*- coding: utf-8 -*-
{
    'name': 'Helpdesk Portal - Crear Tickets',
    'version': '1.1',
    'category': 'Services/Helpdesk',
    'summary': 'Permite a los clientes del portal crear tickets de helpdesk extendidos',
    'description': """
        Este módulo extiende el portal de Helpdesk para permitir que los 
        usuarios del portal creen nuevos tickets directamente desde su cuenta.
        Incluye campos de Categoría, Impacto, Urgencia y adjuntos.
    """,
    'author': 'Custom',
    'depends': ['helpdesk', 'portal'],
    'data': [
        'views/portal_templates.xml',
        'views/helpdesk_ticket_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
