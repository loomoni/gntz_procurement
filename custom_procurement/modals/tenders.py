from odoo import models, fields, api, _


class GntzTenders(models.Model):
    _name = "gntz.tenders"
    _description = "Gntz Tenders"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "date"

    STATE_SELECTION = [
        ("draft", "Draft"),
        ("submit", "Submitted"),
        ("review", "Line Manager Reviewed"),
        ("verify", "Procurement Approve"),
        ("publish", "AD Approved $ Published"),
        ("closed", "Closed"),
        ("reject", "Rejected"),
        ("cancel", "Cancelled"),
    ]

    @api.multi
    def btn_submit(self):
        self.write({'state': 'submit'})
        return True

    @api.multi
    def btn_line_manager_review(self):
        self.write({'state': 'review'})
        return True

    @api.multi
    def btn_procurement_verify(self):
        self.write({'state': 'verify'})
        return True

    @api.multi
    def btn_approve_and_publish_to_website(self):
        self.write({'state': 'publish'})
        return True

    name = fields.Char(string='Tender Name', states={'draft': [('readonly', False)]}, required=True)
    tender_requisition_id = fields.Many2one(comodel_name="requisition.purchase.purchase", string='Purchase Requisition',
                                            required=True)
    date = fields.Date(string='Posted Date', default=fields.Date.today())
    end_date = fields.Date(string='End Submission Date')
    attachment = fields.Binary(string="TOR Attachment", attachment=True, store=True)
    attachment_name = fields.Char('Attachment')
    state = fields.Selection(STATE_SELECTION, index=True, track_visibility='onchange', required=True, copy=False,
                             default='draft')
    description = fields.Html(string='Tender Description')
    bidders_line_ids = fields.One2many(comodel_name="tenders.applicants", inverse_name="tender_id", string="Bidders ID")


class TendersApplicants(models.Model):
    _name = "tenders.applicants"
    _description = "tenders applicants"

    name = fields.Char(string='Applicant Name')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    attachment = fields.Binary(string="TOR Attachment", attachment=True, store=True)
    attachment_name = fields.Char('Attachment')
    tender_id = fields.Many2one(comodel_name="gntz.tenders", string="Subject")
