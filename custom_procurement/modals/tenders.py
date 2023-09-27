from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError
from odoo.fields import Date, _logger


class GntzTenders(models.Model):
    _name = "gntz.tenders"
    _description = "Gntz Tenders"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    STATE_SELECTION = [
        ("draft", "Draft"),
        ("submit", "Submitted"),
        ("review", "Line Manager Reviewed"),
        ("verify", "Procurement Approve"),
        ("Published", "AD Approved & Published"),
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
    tender_number = fields.Char(string='Tender Number', states={'draft': [('readonly', False)]}, )
    tender_requisition_id = fields.Many2one(comodel_name="requisition.purchase.purchase", string='Purchase Requisition',
                                            required=True)
    date = fields.Date(string='Posted Date', default=fields.Date.today())
    end_date = fields.Date(string='End Submission Date')
    tender_type = fields.Selection([('Goods', 'Goods'), ('Services', 'Services'), ('Works', 'Works')],
                                   string="Tender Type",
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
    # order = 'total_score desc'

    name = fields.Char(string='Applicant Name')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    company = fields.Char(string='Company')
    total_score = fields.Integer(string="Total Score", compute="_compute_applicant_total_score", default=0)
    applicant_score_lines_ids = fields.One2many(comodel_name="applicant.scores",
                                                inverse_name="applicants_score_ids", string='Evaluation Template')
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

    @api.depends('applicant_score_lines_ids')
    def _compute_applicant_total_score(self):
        for rec in self:
            sub_total = 0
            rec.total_score = sub_total + sum(line.sub_total_score for line in rec.applicant_score_lines_ids)

        _order = 'total_score desc'
    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     # Default order by 'total_score' descending
    #     if order is None:
    #         order = 'total_score desc'
    #
    #     return super(TendersApplicants, self).search(args, offset, limit, order, count)


class ApplicantScores(models.Model):
    _name = "applicant.scores"
    _description = "Applicant Scores"
    _rec_name = "evaluation_template"

    evaluation_template = fields.Many2one(comodel_name="evaluation.criteria.template", string="Evaluation Criteria",
                                          store=True)
    applicants_score_ids = fields.Many2one(comodel_name='tenders.applicants', string="Applicant IDS")
    sub_total_score = fields.Integer(string="Sub Total Score", compute="_sub_total_score_compute")
    user_id = fields.Many2one(comodel_name='res.users', string='Committee', default=lambda self: self.env.user,
                              readonly=True)
    score_lines_ids = fields.One2many(comodel_name="applicant.scores.lines", inverse_name="applicants_score_line_ids",
                                      string="Score IDS")

    @api.depends('score_lines_ids')
    def _sub_total_score_compute(self):
        for rec in self:
            rec.sub_amount = 0
            rec.sub_total_score = rec.sub_amount + sum(line.score for line in rec.score_lines_ids)
        # sub_total = 0
        # self._sub_total_score_compute = sub_total + sum(line.score for line in self.score_lines_ids)

    # @api.onchange('evaluation_template')
    # # @api.depends('evaluation_template')
    # def update_score_lines(self):
    #     if self.evaluation_template:
    #         criteria_lines = self.evaluation_template.lines_ids
    #         # Clear existing score lines
    #         self.score_lines_ids.unlink()
    #         # Create new score lines with criteria names and expected remarks
    #         score_lines = []
    #         for criteria_line in criteria_lines:
    #             score_lines.append((0, 0, {
    #                 'criteria': criteria_line.criteria,
    #                 'max_marks': criteria_line.expected_remarks,
    #                 'applicants_score_line_ids': self.applicants_score_ids.id
    #             }))
    #         self.score_lines_ids = score_lines
    # self.write({'score_lines_ids': score_lines})

    # @api.onchange('evaluation_template')
    # def update_score_lines(self):
    #     if self.evaluation_template:
    #         criteria_lines = self.evaluation_template.lines_ids
    #         # Clear existing score lines
    #         self.score_lines_ids.unlink()
    #         # Create new score lines with criteria names and expected remarks
    #         score_lines = []
    #         for criteria_line in criteria_lines:
    #             score_lines.append((0, 0, {
    #                 'criteria': criteria_line.criteria,
    #                 'max_marks': criteria_line.expected_remarks,
    #                 'applicants_score_line_ids': self.applicants_score_ids.id
    #             }))
    #
    #         # Link the created score lines with the current applicant score
    #         self.write({'score_lines_ids': score_lines})

    # @api.onchange('evaluation_template')
    # def update_score_lines(self):
    #     if self.evaluation_template:
    #         criteria_lines = self.evaluation_template.lines_ids
    #         # Clear existing score lines
    #         self.score_lines_ids.unlink()
    #         # Create new score lines with criteria names and expected remarks
    #         score_lines = []
    #         for criteria_line in criteria_lines:
    #             score_lines.append((0, 0, {
    #                 'criteria': criteria_line.criteria,
    #                 'max_marks': criteria_line.expected_remarks,
    #                 'applicants_score_line_ids': self.applicants_score_ids.id
    #             }))
    #
    #         # Link the created score lines with the current applicant score
    #         self.score_lines_ids = score_lines
    #
    #         # Save the current record to ensure the lines are persisted
    #         self.ensure_one()
    #         self.write({'score_lines_ids': [(6, 0, [line[2] for line in score_lines])]})

    # @api.onchange('evaluation_template')
    # def update_score_lines(self):
    #     if self.evaluation_template:
    #         criteria_lines = self.evaluation_template.lines_ids
    #         # Clear existing score lines
    #         self.score_lines_ids.unlink()
    #         # Create new score lines with criteria names and expected remarks
    #         for criteria_line in criteria_lines:
    #             new_score_line = self.env['applicant.scores.lines'].create({
    #                 'criteria': criteria_line.criteria,
    #                 'max_marks': criteria_line.expected_remarks,
    #                 'applicants_score_line_ids': self.applicants_score_ids.id
    #             })
    #             self.score_lines_ids += new_score_line

    # @api.onchange('evaluation_template')
    # def update_score_lines(self):
    #     if self.evaluation_template:
    #         # Clear existing score lines
    #         self.score_lines_ids.unlink()
    #
    #         # Fetch all criteria lines associated with the selected evaluation template
    #         criteria_lines = self.env['evaluation.criteria.template.line'].search([
    #             ('evaluation_id', '=', self.evaluation_template.id)
    #         ])
    #
    #         # Create new score lines with criteria names and expected remarks
    #         score_lines = []
    #         for criteria_line in criteria_lines:
    #             score_lines.append((0, 0, {
    #                 'criteria': criteria_line.criteria,
    #                 'max_marks': criteria_line.expected_remarks,
    #             }))
    #
    #         # Link the created score lines with the current applicant score
    #         self.score_lines_ids = score_lines

    # @api.onchange('evaluation_template')
    # def update_score_lines(self):
    #     if self.evaluation_template:
    #         # Clear existing score lines
    #         self.score_lines_ids.unlink()
    #
    #         # Fetch all criteria lines associated with the selected evaluation template
    #         criteria_lines = self.env['evaluation.criteria.template.line'].search([
    #             ('evaluation_id', '=', self.evaluation_template.id)
    #         ])
    #
    #         # Create new score lines with criteria names and expected remarks
    #         score_lines = []
    #         for criteria_line in criteria_lines:
    #             score_line_vals = {
    #                 'criteria': criteria_line.criteria,
    #                 'max_marks': criteria_line.expected_remarks,
    #                 'applicants_score_line_ids': self.applicants_score_ids.id
    #             }
    #             score_lines.append((0, 0, score_line_vals))
    #
    #         # Create the score lines using create method
    #         self.env['applicant.scores.lines'].create(score_lines)

    # @api.onchange('evaluation_template')
    # def update_score_lines(self):
    #     if self.evaluation_template:
    #         # Clear existing score lines
    #         self.score_lines_ids.unlink()
    #
    #         # Fetch all criteria lines associated with the selected evaluation template
    #         criteria_lines = self.env['evaluation.criteria.template.line'].search([
    #             ('evaluation_id', '=', self.evaluation_template.id)
    #         ])
    #
    #         # Create new score lines with criteria names and expected remarks
    #         score_lines = []
    #         for criteria_line in criteria_lines:
    #             score_line = self.env['applicant.scores.lines'].create({
    #                 'criteria': criteria_line.criteria,
    #                 'max_marks': criteria_line.expected_remarks,
    #                 'applicants_score_line_ids': self.applicants_score_ids.id
    #             })
    #             score_lines.append(score_line.id)
    #
    #         # Update the score_lines_ids field with the newly created score lines
    #         self.write({'score_lines_ids': [(6, 0, score_lines)]})

    # @api.onchange('evaluation_template')
    # def update_score_lines(self):
    #     if self.evaluation_template:
    #         # Clear existing score lines
    #         self.score_lines_ids.unlink()
    #
    #         # Create new score lines with criteria names and expected remarks
    #         score_lines = []
    #         for criteria_line in self.evaluation_template.lines_ids:
    #             score_line = self.env['applicant.scores.lines'].create({
    #                 'criteria': criteria_line.criteria,
    #                 'max_marks': criteria_line.expected_remarks,
    #                 'applicants_score_line_ids': self.applicants_score_ids.id
    #             })
    #             score_lines.append(score_line.id)
    #
    #         # Update the score_lines_ids field with the newly created score lines
    #         self.write({'score_lines_ids': [(6, 0, score_lines)]})

    # def create_score_lines(self, criteria_line):
    #     score_line = self.env['applicant.scores.lines'].create({
    #         'criteria': criteria_line.criteria,
    #         'max_marks': criteria_line.expected_remarks,
    #         'applicants_score_line_ids': self.applicants_score_ids.id
    #     })
    #     return score_line
    #
    # @api.onchange('evaluation_template')
    # def update_score_lines(self):
    #     if self.evaluation_template:
    #         # Clear existing score lines
    #         self.score_lines_ids.unlink()
    #
    #         # Fetch all criteria lines associated with the selected evaluation template
    #         criteria_lines = self.evaluation_template.lines_ids
    #
    #         # Create new score lines with criteria names and expected remarks
    #         score_lines = []
    #         for criteria_line in criteria_lines:
    #             score_line = self.create_score_lines(criteria_line)
    #             score_lines.append(score_line.id)
    #
    #         # Update the score_lines_ids field with the newly created score lines
    #         self.write({'score_lines_ids': [(6, 0, score_lines)]})

    @api.multi
    @api.onchange('evaluation_template')
    def update_score_lines(self):
        for record in self:
            if record.evaluation_template:
                # Clear existing score lines
                record.score_lines_ids.unlink()

                # Fetch all criteria lines associated with the selected evaluation template
                criteria_lines = record.evaluation_template.lines_ids

                # Create new score lines with criteria names and expected remarks
                score_lines = []
                for criteria_line in criteria_lines:
                    score_line = self.env['applicant.scores.lines'].create({
                        'criteria': criteria_line.criteria,
                        'max_marks': criteria_line.expected_remarks,
                        'applicants_score_line_ids': record.applicants_score_ids.id
                    })
                    score_lines.append(score_line.id)

                # Update the score_lines_ids field with the newly created score lines
                record.score_lines_ids = [(6, 0, score_lines)]


class ApplicantScoresLines(models.Model):
    _name = "applicant.scores.lines"
    _description = "Applicant Scores"

    criteria = fields.Char(string="criteria name", readonly=True, store=True)
    max_marks = fields.Integer(string="Maximum Marks", readonly=True, store=True)
    score = fields.Integer(string="Rate Score", required=True, store=True)
    applicants_score_line_ids = fields.Many2one(comodel_name='tenders.applicants', string="Applicant IDS")

    @api.constrains('score', 'max_marks')
    @api.onchange('score', 'max_marks')
    def _check_score(self):
        for record in self:
            if record.score > record.max_marks:
                raise exceptions.ValidationError("Score cannot exceed the maximum marks.")


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
