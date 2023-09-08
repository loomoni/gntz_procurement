from odoo import models, fields, api, _


class WorkPlan(models.Model):
    _name = "work.plan"
    _description = "Procurement Work Plan"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref_no = fields.Char(string="Ref No")

    name = fields.Many2one(comodel_name="procurement.plan", string="Department Procurement Plan", required=True)
    subjected = fields.Char(string="Subject", required=True)
    date = fields.Date(string="Date", required=True)
    addressed_to = fields.Char(string="Addressed To", required=True)
    description = fields.Html("Work Plan Description")
    procurement_plan = fields.Many2one(comodel_name="", string="Subject")
