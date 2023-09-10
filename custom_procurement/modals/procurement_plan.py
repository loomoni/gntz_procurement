from odoo import api, fields, models, _
import time
from datetime import datetime, date, time, timedelta
from odoo import exceptions


class ProcurementPlan(models.Model):
    _name = "procurement.plan"
    _description = "Procurement Plan"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _default_department(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1).department_id.id

    STATE_SELECTION = [
        ("draft", "Draft"),
        ("submit", "Submitted"),
        ("approve", "Approved"),
        ("purchase", "Purchased"),
        ("closed", "Closed"),
        ("reject", "Rejected"),
        ("cancel", "Cancelled"),
    ]

    @api.depends('line_ids.price_total')
    def _amount_all(self):
        for order in self:
            amount = 0.0
            for line in order.line_ids:
                amount += line.price_total
            order.update({'amount_total': amount})

    @api.multi
    def button_submit(self):
        self.write({'state': 'submit'})
        return True

    @api.multi
    def button_procurement_approve(self):
        self.write({'state': 'approve'})
        procurement_data = self.env['procurement.plan.version.line']
        for line in self:
            procurement_data.create({
                'requested': line.requested_by.id,
                'version_id': line.version_id.id,
                'department_id': line.department_id.id,
                'amount': line.amount_total,
                'version_name': line.version_name,
            })
        return True

    @api.multi
    def back_to_draft_procurement(self):
        self.write({'state': 'draft'})
        return True

    @api.multi
    def reject(self):
        self.write({'state': 'reject'})
        return True

    name = fields.Char(string="Name")
    version_id = fields.Many2one('procurement.plan.version', string='Procurement Plan Version', readonly=True,
                                 required=True,
                                 states={'draft': [('readonly', False)]})
    version_name = fields.Char(string="Plan Version", related='version_id.name')
    requested_by = fields.Many2one('res.users', 'Requested by', required=True, track_visibility='onchange',
                                   default=lambda self: self._uid,
                                   readonly=True, states={'draft': [('readonly', False)]})
    department_id = fields.Many2one('hr.department', string='Department', required=True, track_visibility='onchange',
                                    readonly=True,
                                    states={'draft': [('readonly', False)], 'submit': [('readonly', False)]},
                                    default=_default_department)
    state = fields.Selection(STATE_SELECTION, index=True, track_visibility='onchange', required=True, copy=False,
                             default='draft')
    amount_total = fields.Float(string='Total', store=True, readonly=True, compute='_amount_all')
    line_ids = fields.One2many(comodel_name='procurement.plan.line', inverse_name="plan_id",
                               string='Products to Purchase')


class ProcurementPlanLine(models.Model):
    _name = "procurement.plan.line"
    _description = "Procurement Plan Line"

    plan_id = fields.Many2one(comodel_name="procurement.plan", string='Procurement Plan')
    product_id = fields.Many2one('product.product', 'Product', domain=[('purchase_ok', '=', True)],
                                 track_visibility='onchange', required=True)
    price_unit = fields.Float(string='Estimated')
    product_qty = fields.Float(string="Planned Quantity", required=True, track_visibility='onchange')
    price_total = fields.Float(compute='_compute_amount', string='Total', store=True)
    project_name = fields.Char(String="Project Name")
    description = fields.Char(String="Activity Description")
    source_fund = fields.Char(String="Source of Fund")

    @api.depends('price_unit', 'product_qty')
    def _compute_amount(self):
        for rec in self:
            rec.price_total = rec.price_unit * rec.product_qty