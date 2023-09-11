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

    @api.multi
    def btn_user_submit(self):
        self.write({'state': 'submit'})
        return True

    @api.multi
    def btn_line_manager_review(self):
        self.write({'state': 'review'})
        return True

    @api.multi
    def btn_back_draft(self):
        self.write({'state': 'draft'})
        return True

    @api.multi
    def btn_ad_approve(self):
        self.write({'state': 'approve'})
        return True

    @api.multi
    def btn_back_line_manager(self):
        self.write({'state': 'submit'})
        return True

    @api.multi
    def btn_reject(self):
        self.write({'state': 'reject'})
        return True

    ref_no = fields.Char(string="Ref No")
    name = fields.Many2one(comodel_name="procurement.plan", string="Department Procurement Plan", required=True)
    subjected = fields.Char(string="Subject", required=True)
    state = fields.Selection(SELECTION, default='draft', tack_visibility='onchange')
    date = fields.Date(string="Date", required=True)
    addressed_to = fields.Char(string="Addressed To", required=True)
    description = fields.Html("Work Plan Description")
    department_id = fields.Many2one(comodel_name="hr.department", required=True, string="Department",
                                    default=_default_department)
    procurement_plan = fields.Many2one(comodel_name="", string="Subject")
