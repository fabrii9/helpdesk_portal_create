# -*- coding: utf-8 -*-
from odoo import models, fields


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    ticket_category = fields.Selection([
        ('unexpected', 'Comportamiento no esperado'),
        ('doubt', 'Duda de uso'),
        ('consulting', 'Consultoría'),
        ('commercial', 'Consulta Comercial'),
    ], string='Categoría')

    impact = fields.Selection([
        ('low', 'Bajo (Otros)'),
        ('medium', 'Medio (Afecta a un sector de la organización)'),
        ('high', 'Alto (Afecta a toda la organización)'),
    ], string='Impacto')

    urgency = fields.Selection([
        ('low', 'Bajo (Otros)'),
        ('medium', 'Medio (Interrupción de una operación no crítica o problemas operativos de la principal)'),
        ('high', 'Alto (Interrupción de la operación principal o elevado riesgo financiero)'),
    ], string='Urgencia')
