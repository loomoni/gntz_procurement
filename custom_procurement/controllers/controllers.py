from addons.website.controllers.main import Website
from odoo import http
from odoo.http import request
from odoo.tools import datetime


# class WebsiteTenderController(http.Controller):
class TenderWebsite(http.Controller):
    @http.route(['/tenders'], type='http', auth="public", website=True)
    def tenders_page(self):
        # Get today's date
        today_date = datetime.now().date()
        tenders = http.request.env['gntz.tenders'].search([('state', '=', 'publish'), ('end_date', '>', today_date)],
                                                          order='create_date desc')
        return http.request.render('custom_procurement.website_tender_template', {'docs': tenders})

    @http.route(['/tenders/<model("gntz.tenders"):tender>'], type='http', auth="public",
                website=True)
    def tender_detail(self, tender):
        return http.request.render('custom_procurement.website_tender_detail_template', {'doc': tender})


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
        # attachment = post.get('attachment')

        # Save data to the 'tenders.applicants' model
        applicants_model = request.env['tenders.applicants']
        applicants_model.create({
            'tender_id': int(tender_id),
            'name': name,
            'email': email,
            'phone': phone,
            'company': company,
            # 'attachment': attachment,
            # Other fields as needed
        })

        # Redirect to a success page or provide feedback to the user
        return http.request.redirect('/application_success')
