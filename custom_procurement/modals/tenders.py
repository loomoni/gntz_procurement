from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.fields import Date


class GntzTenders(models.Model):
    _name = "gntz.tenders"
    _description = "Gntz Tenders"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    STATE_SELECTION = [
        ("draft", "Draft"),
        ("submit", "Submitted"),
        ("review", "Line Manager Reviewed"),
        ("verify", "Procurement Approve"),
        ("Published", "AD Approved $ Published"),
        ("Bid Evaluation", "Committee Approved"),
        ("Contract Awarded", "Contract Awarded"),
        ("Closed", "Closed"),
        ("Rejected", "Rejected"),
        ("Canceled", "Cancelled"),
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
        self.write({'state': 'Published'})
        return True

    @api.multi
    def committee_approved(self):
        # check if you have at least three commit members
        if len(self.tender_opening_committee_line_ids) >= 3:
            self.write({'state': 'Bid Evaluation'})
            return True
        else:
            raise ValidationError('You need at least 3 committee members to be Approved')

    @api.multi
    def contract_awarded(self):
        self.write({'state': 'Contract Awarded'})
        return True

    name = fields.Char(string='Tender Name', states={'draft': [('readonly', False)]}, required=True)
    tender_number = fields.Char(string='Tender Number', states={'draft': [('readonly', False)]},)
    tender_requisition_id = fields.Many2one(comodel_name="requisition.purchase.purchase", string='Purchase Requisition',
                                            required=True)
    date = fields.Date(string='Posted Date', default=fields.Date.today())
    end_date = fields.Date(string='End Submission Date')
    tender_type = fields.Selection([('Goods', 'Goods'), ('Services', 'Services'), ('Works', 'Works')], string="Tender Type",
                            required=True)
    branch = fields.Many2one(comodel_name="hr.branches", string="Branch", store=True)
    attachment = fields.Binary(string="TOR Attachment", attachment=True, store=True)
    attachment_name = fields.Char('Attachment')
    state = fields.Selection(STATE_SELECTION, index=True, track_visibility='onchange', required=True, copy=False,
                             default='draft')
    description = fields.Html(string='Tender Description')
    bidders_line_ids = fields.One2many(comodel_name="tenders.applicants", inverse_name="tender_id", string="Bidders ID")
    tender_opening_committee_line_ids = fields.One2many(comodel_name="tenders.opening.committee",
                                                        inverse_name="tender_committee_id", string="Tender Committee")

    evaluation_lines_ids = fields.One2many(comodel_name="tender.evaluation.criteria.line",
                                           inverse_name="evaluation_criteria_id", string="Evaluation Criteria Template")


class TendersApplicants(models.Model):
    _name = "tenders.applicants"
    _description = "tenders applicants"

    name = fields.Char(string='Applicant Name')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')

    attachment = fields.Binary(string="Company Profile", attachment=True, store=True)
    attachment_name = fields.Char('Company Profile Attachment')

    business_licence_attachment = fields.Binary(string="Business Licence", attachment=True, store=True)
    business_licence_attachment_name = fields.Char('Business Licence Attachment')

    tin_registration_attachment = fields.Binary(string="TIN & Certificate of registration", attachment=True, store=True)
    tin_registration_attachment_name = fields.Char('TIN & Certificate of registration Attachment')

    technical_proposal = fields.Binary(string="Technical Proposal", attachment=True, store=True)
    technical_proposal_name = fields.Char('Technical Proposal Attachment')

    financial_proposal = fields.Binary(string="Financial Proposal", attachment=True, store=True)
    financial_proposal_name = fields.Char('Financial Proposal Attachment')

    tender_id = fields.Many2one(comodel_name="gntz.tenders", string="Subject")


class TendersOpeningCommittee(models.Model):
    _name = "tenders.opening.committee"
    _description = "tenders opening committee"

    name = fields.Many2one(comodel_name="res.users", string='Committee Member', required=True)
    date = fields.Date(string='Date', default=fields.Date.today())
    position = fields.Selection([('chairperson', 'Chairperson'), ('secretary', 'Secretary'), ('member', 'Member')],
                                string='Position', required=True)
    tender_committee_id = fields.Many2one(comodel_name="gntz.tenders", string="Tender ID", readonly=True)


class TendersEvaluationCriteriaTempalte(models.Model):
    _name = "tender.evaluation.criteria.line"

    name = fields.Many2one(comodel_name="evaluation.criteria.template", string="Tender Evaluation Tempalte")
    evaluation_criteria_id = fields.Many2one(comodel_name="gntz.tenders", string="Evaluation Template ID")


class EvaluationCriteriaTemplate(models.Model):
    _name = "evaluation.criteria.template"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Criteria Template Name")
    type = fields.Selection([('goods', 'Goods'), ('service', 'Services'), ('work', 'Works')], string="Procurement Type",
                            required=True)
    lines_ids = fields.One2many(comodel_name="evaluation.criteria.template.line", inverse_name="evaluation_id")


class EvaluationCriteriaTemplateLine(models.Model):
    _name = "evaluation.criteria.template.line"

    criteria = fields.Text(string="Criteria", required=True)
    type = fields.Selection([('Technical', 'Technical'), ('Financial', 'Financial'), ('Professional', 'Professional')],
                            string="Type", required=True)
    expected_remarks = fields.Integer(string="Expected Remarks", required=True)
    maximum_score = fields.Integer(string="Maximum Score", required=True, default=100)
    evaluation_id = fields.Many2one(comodel_name="evaluation.criteria.template", string="Evaluation ID")
