from odoo import models, fields, api, _


class WorkPlan(models.Model):
    _name = "work.plan"
    _description = "Procurement Work Plan"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _default_department(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1).department_id.id

    SELECTION = [
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('review', 'Line Manager Review'),
        ('approve', 'AD Approved'),
        ('reject', 'Rejected'),
    ]

    ref_no = fields.Char(string="Ref No")
    name = fields.Many2one(comodel_name="procurement.plan", string="Department Procurement Plan", required=True)
    subjected = fields.Char(string="Subject", required=True)
    state = fields.Selection(SELECTION, default='draft', tack_visibility='onchange')
    date = fields.Date(string="Date", required=True)
    addressed_to = fields.Char(string="Addressed To", required=True)
    description = fields.Html("Work Plan Description")
    department_id = fields.Many2one(comodel_name="hr.department", required=True, string="Department", default=_default_department)
    procurement_plan = fields.Many2one(comodel_name="", string="Subject")
