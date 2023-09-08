# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import datetime
from odoo.http import request


class ProcurementPlanVersion(models.Model):
    _name = "procurement.plan.version"
    _description = "Procurement Plan Version"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "date_start desc"

    STATE_SELECTION = [
        ("draft", "Draft"),
        ("released", "Released"),
        ("submit", "Submitted"),
        ("approved", "Approved"),
        ("review", "Reviewed"),
        ("closed", "Closed"),
        ("cancel", "Cancelled"),
        ("reject", "Rejected"),
    ]

    # @api.multi
    # def button_release(self):
    #     user_id = request.session.uid
    #     print("Session Key", user_id)

    name = fields.Char(string='Version Name', required=True, index=True)
    active = fields.Boolean('Active', default=True)
    date_start = fields.Date(string='Validity Start Date', required=True,
                             default=datetime.strptime('%s-01-01' % (datetime.now().year + 1), '%Y-%m-%d').strftime(
                                 '%Y-%m-%d'),
                             readonly=True, states={'draft': [('readonly', False)], 'submit': [('readonly', False)]})
    date_end = fields.Date(string='Validity End Date', required=True,
                           default=datetime.strptime('%s-12-31' % (datetime.now().year + 1), '%Y-%m-%d').strftime(
                               '%Y-%m-%d'),
                           readonly=True, states={'draft': [('readonly', False)], 'submit': [('readonly', False)]})
    state = fields.Selection(STATE_SELECTION, index=True, track_visibility='onchange',
                             readonly=True, required=True, copy=False, default='draft')
    line_ids = fields.One2many('procurement.plan.version.line', 'version_id', string='Procurement Plan Version Lines',
                               readonly=True)


class ProcurementPlanVersionLine(models.Model):
    _name = "procurement.plan.version.line"
    _description = "Procurement Plan Version Line"
    _order = "version_id"

    STATE_PLAN_SELECTION = [
        ("draft", "Draft"),
        ("released", "Released"),
        ("approved", "Approved"),
        ("deployed", "Deployed"),
        ("reject", "Rejected"),
        ("cancel", "Cancelled"),
    ]

    version_id = fields.Many2one("procurement.plan.version", "Procurement Plan Version ID", index=True, required=True,
                                 ondelete='cascade')
