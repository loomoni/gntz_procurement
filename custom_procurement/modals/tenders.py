from odoo import models, fields, api, _


class GntzTenders(models.Model):
    _name = "gntz.tenders"
    _description = "Gntz Tenders"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "date"

    STATE_SELECTION = [
        ("draft", "Draft"),
        ("submit", "Submitted"),
        ("review", "Reviewed"),
        ("approve", "Approved"),
        ("publish", "Published"),
        ("closed", "Closed"),
        ("reject", "Rejected"),
        ("cancel", "Cancelled"),
    ]

    name = fields.Char(string='Tender Name', states={'draft': [('readonly', False)]}, required=True)
    tender_requisition_id = fields.Many2one(comodel_name="requisition.purchase.purchase", string='Purchase Requisition', required=True)
    date = fields.Date(string='Posted Date', default=fields.Date.today())
    end_date = fields.Date(string='End Submission Date')
    attachment = fields.Binary(string="TOR Attachment", attachment=True, store=True)
    attachment_name = fields.Char('Attachment')
    state = fields.Selection(STATE_SELECTION, index=True, track_visibility='onchange', required=True, copy=False,
                             default='draft')
    description = fields.Html(string='Tender Description')

    @api.multi
    def publish_to_website(self):
        self.write({'state': 'publish'})
        return True


class TendersApplicants(models.Model):
    _name = "tenders.applicants"
    _description = "tenders applicants"

    name = fields.Char(string='Applicant Name')
    email = fields.Date(string='Email')
    phone = fields.Date(string='Phone')
    attachment = fields.Binary(string="TOR Attachment", attachment=True, store=True)
    attachment_name = fields.Char('Attachment')
