# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.helpdesk.controllers.portal import CustomerPortal as HelpdeskCustomerPortal
from odoo.exceptions import ValidationError, UserError


class CustomerPortal(HelpdeskCustomerPortal):

    def _get_allowed_teams(self):
        """Retorna los equipos de helpdesk visibles en el portal."""
        return request.env['helpdesk.team'].sudo().search([
            ('privacy_visibility', '=', 'portal'),
        ])

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        values['can_create_ticket'] = bool(self._get_allowed_teams())
        return values

    @http.route(['/my/tickets/new'], type='http', auth="user", website=True)
    def portal_create_ticket(self, **kwargs):
        values = self._prepare_portal_layout_values()
        values.update({
            'page_name': 'ticket',
            'teams': self._get_allowed_teams(),
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

        if not post.get('team_id'):
            error['team_id'] = True
            error_message.append(_('Debe seleccionar un equipo de helpdesk.'))
        else:
            team = request.env['helpdesk.team'].sudo().browse(int(post.get('team_id')))
            if not team.exists() or team.privacy_visibility != 'portal':
                error['team_id'] = True
                error_message.append(_('El equipo seleccionado no es válido.'))

        if error:
            values = self._prepare_portal_layout_values()
            values.update({
                'page_name': 'ticket',
                'teams': self._get_allowed_teams(),
                'error': error,
                'error_message': error_message,
                'form_data': post,
            })
            return request.render("helpdesk_portal_create.portal_create_ticket_form", values)

        # Obtener el partner del usuario actual
        partner = request.env.user.partner_id
        if not partner:
            raise UserError(_('No se encontró un contacto asociado a su usuario.'))

        team_id = int(post.get('team_id'))
        team = request.env['helpdesk.team'].sudo().browse(team_id)

        # Crear el ticket con sudo (el portal user no tiene permisos de creación)
        ticket_vals = {
            'name': post.get('name').strip(),
            'team_id': team_id,
            'partner_id': partner.id,
            'partner_name': partner.name,
            'partner_email': partner.email,
            'partner_phone': partner.phone or partner.mobile,
            'description': post.get('description', ''),
        }

        if post.get('priority'):
            ticket_vals['priority'] = post.get('priority')

        ticket = request.env['helpdesk.ticket'].sudo().create(ticket_vals)

        return request.redirect('/my/ticket/%s' % ticket.id)
