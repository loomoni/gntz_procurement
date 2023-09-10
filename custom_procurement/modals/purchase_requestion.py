from odoo import api, fields, models, _
import time
from datetime import datetime, date, time, timedelta
from odoo import exceptions


class PurchaseRequisition(models.Model):
    _name = "requisition.purchase.purchase"
    _description = "Purchase Requisition"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "project_name"

    STATE_SELECTION = [
        ("draft", "Draft"),
        ("request", "Submit Request"),
        ("tender", "Competitive Tender"),
        ("quotation", "Quotation"),
        ("reject", "Reject"),
        ("back_draft", "Back to Draft"),
    ]

    @api.multi
    def button_submit_request(self):
        self.write({'state': 'request'})
        return True

    @api.multi
    def button_competitive_tender(self):
        self.write({'state': 'tender'})
        return True

    @api.multi
    def button_low_value_quotation(self):
        self.write({'state': 'quotation'})
        return True

    @api.multi
    def button_send_back_draft(self):
        self.write({'state': 'draft'})
        return True

    project_name = fields.Char(string="Project Name", required=True)
    activity_name = fields.Char(string="Activity Name", required=True)

    activity_budget_year = fields.Char(string="Activity Budget year", required=True)
    implementation_date = fields.Date(string="Implementation Date", required=True)

    delivery_place = fields.Char(string="Delivery Place")
    other_details = fields.Char(string="Other Details")

    date = fields.Date(string="Date", required=True)
    department = fields.Many2one(string="Department", comodel_name="hr.department", required=True)

    budget_source = fields.Char(string="Source Of Budget", required=True)
    customer = fields.Many2one(string="Customer", comodel_name="res.partner", required=True)

    job = fields.Char(string="Job")
    class_code = fields.Char(string="Class Code")

    state = fields.Selection(STATE_SELECTION, index=True, track_visibility='onchange',
                             readonly=True, required=True, copy=False, default='draft')
    purchase_requisition_line_ids = fields.One2many(comodel_name='requisition.purchase.purchase.line',
                                                    inverse_name="purchase_requisition_id",
                                                    string='Products to Purchase')
    purchase_requisition_attachment_ids = fields.One2many(comodel_name='purchase.requisition.attachment.line',
                                                          inverse_name="purchase_requisition_attachment_id",
                                                          string='Products to Purchase attachment')


class PurchaseRequisitionLine(models.Model):
    _name = "requisition.purchase.purchase.line"
    _description = "Purchase Requisition Line"

    item = fields.Many2one(comodel_name="product.product", string="Item")
    item_specification = fields.Char(string="Item Specification")
    quantity = fields.Char(string="Quantity")
    unit = fields.Char(string="Unit")
    color = fields.Char(string="Color")
    dimension = fields.Char(string="Dimension")
    remark = fields.Char(string="Remark")
    purchase_requisition_id = fields.Many2one(comodel_name="requisition.purchase.purchase",
                                                       string='Purchase Requisition ID')


class PurchaseRequisitionAttachmentLine(models.Model):
    _name = "purchase.requisition.attachment.line"
    _description = "Purchase Requisition Line"

    name_attachment = fields.Char(String="Name", required=True)
    attachment = fields.Binary(string="Attachment", attachment=True, store=True, required=True)
    attachment_name = fields.Char('Attachment')
    purchase_requisition_attachment_id = fields.Many2one(comodel_name="requisition.purchase.purchase",
                                                         string='Purchase Requisition attachement ID')
