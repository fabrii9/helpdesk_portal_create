# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.helpdesk.controllers.portal import CustomerPortal as HelpdeskCustomerPortal
from odoo.exceptions import ValidationError, UserError


class CustomerPortal(HelpdeskCustomerPortal):

    def _get_default_team(self):
        """Retorna el primer equipo de helpdesk visible en el portal."""
        return request.env['helpdesk.team'].sudo().search([
            ('privacy_visibility', '=', 'portal'),
        ], limit=1)

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        values['can_create_ticket'] = bool(self._get_default_team())
        return values

    @http.route(['/my/tickets/new'], type='http', auth="user", website=True)
    def portal_create_ticket(self, **kwargs):
        values = self._prepare_portal_layout_values()
        values.update({
            'page_name': 'ticket',
            'error': {},
            'error_message': [],
            'form_data': {},
        })
        return request.render("helpdesk_portal_create.portal_create_ticket_form", values)

    @http.route(['/my/tickets/new/submit'], type='http', auth="user", website=True, methods=['POST'])
    def portal_create_ticket_submit(self, **post):
        error = {}
        error_message = []

        # Validaciones
        if not post.get('name', '').strip():
            error['name'] = True
            error_message.append(_('El asunto del ticket es obligatorio.'))

        if not post.get('ticket_category'):
            error['ticket_category'] = True
            error_message.append(_('Debe seleccionar una categoría.'))

        if not post.get('impact'):
            error['impact'] = True
            error_message.append(_('Debe seleccionar el impacto.'))

        if not post.get('urgency'):
            error['urgency'] = True
            error_message.append(_('Debe seleccionar la urgencia.'))

        team = self._get_default_team()
        if not team:
            error_message.append(_('No hay un equipo de helpdesk configurado para el portal. Contacte al administrador.'))

        if error or error_message:
            values = self._prepare_portal_layout_values()
            values.update({
                'page_name': 'ticket',
                'error': error,
                'error_message': error_message,
                'form_data': post,
            })
            return request.render("helpdesk_portal_create.portal_create_ticket_form", values)

        # Obtener el partner del usuario actual
        partner = request.env.user.partner_id
        if not partner:
            raise UserError(_('No se encontró un contacto asociado a su usuario.'))

        # Crear el ticket con sudo (el portal user no tiene permisos de creación)
        ticket_vals = {
            'name': post.get('name').strip(),
            'team_id': team.id,
            'partner_id': partner.id,
            'partner_name': partner.name,
            'partner_email': partner.email,
            'partner_phone': partner.phone or getattr(partner, 'mobile', False) or '',
            'description': post.get('description', ''),
            'ticket_category': post.get('ticket_category'),
            'impact': post.get('impact'),
            'urgency': post.get('urgency'),
        }

        if post.get('priority'):
            ticket_vals['priority'] = post.get('priority')

        ticket = request.env['helpdesk.ticket'].sudo().create(ticket_vals)

        # Procesar adjuntos
        attachments = request.httprequest.files.getlist('attachment')
        for attachment in attachments:
            if attachment.filename:
                request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': attachment.read(),
                    'res_model': 'helpdesk.ticket',
                    'res_id': ticket.id,
                    'type': 'binary',
                })

        return request.redirect('/my/ticket/%s' % ticket.id)
