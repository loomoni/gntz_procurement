import base64

from addons.website.controllers.main import Website
from odoo import http
from odoo.http import request
from odoo.tools import datetime


class CustomHomeWebsite(http.Controller):
    @http.route('/home', type='http', auth="public", website=True)
    def custom_home_page(self, **kw):
        today_date = datetime.now().date()
        open_tenders = http.request.env['gntz.tenders'].search(
            [('state', '=', 'Published'), ('end_date', '>=', today_date)], order='create_date desc')
        awarded_contract_tenders = http.request.env['gntz.tenders'].search([('state', '=', 'Contract Awarded')], order='create_date desc')
        all_tender_states = ['Published', 'Bid Evaluation', 'Contract Awarded', 'Closed', 'Rejected', 'Canceled']
        all_posted_tenders = http.request.env['gntz.tenders'].search([('state', 'in', all_tender_states)],
                                                                     order='create_date '
                                                                           'desc')
        total_tenders = len(all_posted_tenders)
        total_open_tenders = len(open_tenders)
        total_awarded_contract_tenders = len(awarded_contract_tenders)

        return http.request.render('custom_procurement.portal_home_page',
                                   {'docs': all_posted_tenders,
                                    'open_tenders': open_tenders,
                                    'total_tenders': total_tenders,
                                    'total_open_tenders': total_open_tenders,
                                    'awarded_contract_tenders': awarded_contract_tenders,
                                    'total_awarded_contract_tenders': total_awarded_contract_tenders
                                    })


class TenderWebsite(http.Controller):
    @http.route(['/tenders'], type='http', auth="public", website=True)
    def tenders_page(self):
        # Get today's date
        today_date = datetime.now().date()
        all_tender_states = ['Published', 'Bid Evaluation', 'Contract Awarded', 'Closed', 'reject', 'Canceled']
        all_posted_tenders = http.request.env['gntz.tenders'].search([('state', 'in', all_tender_states)],
                                                                     order='create_date '
                                                                           'desc')
        tenders = http.request.env['gntz.tenders'].search([('state', '=', 'Published'), ('end_date', '>', today_date)],order='create_date desc')

        return http.request.render('custom_procurement.tender_page', {'docs': all_posted_tenders})
        # return http.request.render('custom_procurement.website_tender_template', {'docs': tenders})

    @http.route(['/tenders/<model("gntz.tenders"):tender>'], type='http', auth="public",
                website=True)
    def tender_detail(self, tender):
        return http.request.render('custom_procurement.website_tender_detail_template', {'doc': tender})

    @http.route('/page/tenders', type='http', auth="public", website=True)
    def tender_page(self, **kw):
        tenders = request.env['gntz.tenders'].sudo().search([])
        return http.request.render('custom_procurement.tender_page', {'docs': tenders})


class TenderApplicationController(http.Controller):

    @http.route('/apply-tender', type='http', auth="public", website=True)
    def tender_application_form(self, **post):
        # Render the application form page
        return http.request.render('custom_procurement.application_form_template')

    @http.route('/submit_application', type='http', auth="public", website=True)
    def submit_application(self, **post):
        # Retrieve form data
        tender_id = post.get('tender_id')
        name = post.get('name')
        email = post.get('email')
        company = post.get('company')
        phone = post.get('phone')
        # attachment = post.get('attachment_name')

        # Handle file attachment
        attachment = request.httprequest.files.get('attachment')
        attachment_name = attachment.filename if attachment else None
        # Save the attachment and other data to your model (tenders.applicants)
        if attachment:
            # You can save the attachment using the fields.Binary method.
            # Example:
            attachment_data = base64.b64encode(attachment.read())
            applicants_model = request.env['tenders.applicants']
            applicants_model.create({
                'name': name,
                'email': email,
                'phone': phone,
                'company': company,
                'tender_id': tender_id,
                'attachment': attachment_data,
                'attachment_name': attachment_name,
            })

        # Save data to the 'tenders.applicants' model
        # applicants_model = request.env['tenders.applicants']
        # applicants_model.create({
        #     'tender_id': int(tender_id),
        #     'name': name,
        #     'email': email,
        #     'phone': phone,
        #     'company': company,
        #     'attachment': attachment,
        #     # Other fields as needed
        # })

        # Redirect to a success page or provide feedback to the user
        return http.request.redirect('/application_success')
