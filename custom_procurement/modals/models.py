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
        ("review", "Procurement Reviewed"),
        ("approve", "AD Approved"),
        ("closed", "Closed"),
        ("cancel", "Cancelled"),
        ("reject", "Rejected"),
    ]

    @api.multi
    def button_release(self):
        self.write({'state': 'released'})
        return True

    @api.multi
    @api.depends('departmental_procurement_plan_line_ids')
    def button_procurement_review_version(self):
        self.write({'state': 'review'})

        for department_line in self.departmental_procurement_plan_line_ids:
            department_line.state = 'review'
        return True

    @api.multi
    @api.depends('departmental_procurement_plan_line_ids')
    def button_ad_approve(self):
        self.write({'state': 'approve'})
        for department_line in self.departmental_procurement_plan_line_ids:
            department_line.state = 'approve'
        return True

    @api.multi
    def button_reject(self):
        self.write({'state': 'reject'})
        return True

    @api.multi
    def back_procurement(self):
        self.write({'state': 'submit'})
        return True

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
    departmental_procurement_plan_line_ids = fields.One2many('procurement.plan.version.line', 'version_id',
                                                             string='Procurement Plan Version Lines',
                                                             readonly=True)


class ProcurementPlanVersionLine(models.Model):
    _name = "procurement.plan.version.line"
    _description = "Procurement Plan Version Line"
    # _order = "version_id"

    STATE_PLAN_SELECTION = [
        ("draft", "Draft"),
        ("released", "Released"),
        ("review", "Procurement Reviewed"),
        ("approve", "AD Approved"),
        ("deployed", "Deployed"),
        ("reject", "Rejected"),
        ("cancel", "Cancelled"),
    ]

    requested = fields.Many2one(comodel_name="res.users", string="Requested by")
    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    amount = fields.Float(string="Amount")
    version_id = fields.Many2one("procurement.plan.version", "Procurement Plan Version ID", index=True, required=True,
                                 ondelete='cascade')
    state = fields.Selection(STATE_PLAN_SELECTION, default='draft', index=True, track_visibility='onchange',
                             readonly=True, )
    version_name = fields.Char(string="Plan Version", related='version_id.name')
