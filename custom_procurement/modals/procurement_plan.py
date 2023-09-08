import dp as dp

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
        ("released", "Released"),
        ("approved", "Approved"),
        ("purchase", "Purchase"),
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

    version_id = fields.Many2one('procurement.plan.version', string='Procurement Plan Version', readonly=True,
                                 required=True,
                                 states={'draft': [('readonly', False)]})
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






    # product_tmpl_id = fields.Many2one('product.template', string='Product Template',
    #                                   related='product_id.product_tmpl_id')
    # name = fields.Char('Description', track_visibility='onchange')
    # product_qty = fields.Float(string="Planned Quantity", required=True, track_visibility='onchange',
    #                            digits=dp.get_precision('Product Unit of Measure'))
    # product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', track_visibility='onchange',
    #                                  domain="[('category_id', '=', category_uom_id)]")
    # category_uom_id = fields.Many2one(related="product_uom_id.category_id")
    # categ_id = fields.Many2one('product.category', 'Product Category')
    #
    # date_planned = fields.Datetime('Planned Delivery Date', required=True)
    # is_editable = fields.Boolean('Is editable', compute="_compute_is_editable", readonly=True)
    # # currency_id = fields.Many2one('res.currency', string='Currency', related='plan_id.currency_id')
    # price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))
    #
    # saving = fields.Float(string='Target Saving %', default="0.00", required=True)

    # @api.multi
    # @api.depends('product_id', 'name', 'product_qty', 'product_uom_id', 'date_planned', 'price_unit', 'saving')
    # def _compute_is_editable(self):
    #     for record in self:
    #         if record.plan_id.state in ('draft'):
    #             record.is_editable = True
    #         else:
    #             record.is_editable = False
    #     return True
