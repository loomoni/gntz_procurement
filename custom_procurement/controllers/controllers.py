import base64

from addons.auth_signup.controllers.main import AuthSignupHome
from addons.website.controllers.main import Website
from odoo import http
from odoo.http import request
from odoo.tools import datetime


# from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class CustomHomeWebsite(http.Controller):
    @http.route('/home', type='http', auth="public", website=True)
    def custom_home_page(self, **kw):
        today_date = datetime.now().date()
        open_tenders = http.request.env['gntz.tenders'].search(
            [('state', '=', 'Published'), ('end_date', '>=', today_date)], order='create_date desc')
        awarded_contract_tenders = http.request.env['gntz.tenders'].search([('state', '=', 'Contract Awarded')],
                                                                           order='create_date desc')
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
    @http.route(['/all/tenders'], type='http', auth="public", website=True)
    def all_tenders_page(self, tender_type=None, branch=None, **kw):
        # Get today's date
        today_date = datetime.now().date()
        domain = []
        if tender_type:
            domain.append(('tender_type', '=', tender_type))

        if branch:
            domain.append(('branch', '=', int(branch)))

        all_tender_states = ['Published', 'Bid Evaluation', 'Contract Awarded', 'Closed', 'reject', 'Canceled']

        # Concatenate the two domains using the + operator
        combined_domain = [('state', 'in', all_tender_states)] + domain

        all_posted_tenders = http.request.env['gntz.tenders'].search(combined_domain, order='create_date desc')

        branches = request.env['hr.branches'].sudo().search([])

        tenders = http.request.env['gntz.tenders'].search([('state', '=', 'Published'), ('end_date', '>', today_date)],
                                                          order='create_date desc')

        return http.request.render('custom_procurement.all_tenders_page',
                                   {'docs': all_posted_tenders, 'branches': branches})

    # @http.route(['/all/tenders'], type='http', auth="public", website=True)
    # def all_tenders_page(self, tender_type=None, branch=None, **kw):
    #     # Get today's date
    #     today_date = datetime.now().date()
    #     domain = []
    #     if tender_type:
    #         domain.append(('tender_type', '=', tender_type))
    #
    #     if branch:
    #         domain.append(('branch', '=', int(branch)))
    #
    #     all_tender_states = ['Published', 'Bid Evaluation', 'Contract Awarded', 'Closed', 'reject', 'Canceled']
    #     all_posted_tenders = http.request.env['gntz.tenders'].search([('state', 'in', all_tender_states),  domain],
    #                                                                  order='create_date '
    #                                                                        'desc')
    #     branches = request.env['hr.branches'].sudo().search([])
    #     # all_posted_tenders = request.env['gntz.tenders'].sudo().search(domain)
    #     tenders = http.request.env['gntz.tenders'].search([('state', '=', 'Published'), ('end_date', '>', today_date)],
    #                                                       order='create_date desc')
    #
    #     return http.request.render('custom_procurement.all_tenders_page',
    #                                {'docs': all_posted_tenders, 'branches': branches})

    @http.route(['/tenders/<model("gntz.tenders"):tender>'], type='http', auth="public",
                website=True)
    def tender_detail(self, tender):
        # tenders = request.env['gntz.tenders'].sudo().search([])
        return http.request.render('custom_procurement.website_tender_detail_template', {'doc': tender})

    @http.route('/open/tenders', type='http', auth="public", website=True)
    def open_tenders_page(self, tender_type=None, branch=None, **kw):

        domain = []
        if tender_type:
            domain.append(('tender_type', '=', tender_type))

        if branch:
            domain.append(('branch', '=', int(branch)))
        tender_states = ['Published']
        # Concatenate the two domains using the + operator
        combined_domain = [('state', 'in', tender_states)] + domain
        tenders = request.env['gntz.tenders'].sudo().search(combined_domain)
        branches = request.env['hr.branches'].sudo().search([])
        return http.request.render('custom_procurement.open_tenders_page', {'docs': tenders, 'branches': branches})

    @http.route('/awarded/tenders', type='http', auth="public", website=True)
    def awarded_tenders_page(self, tender_type=None, branch=None, **kw):
        domain = []
        if tender_type:
            domain.append(('tender_type', '=', tender_type))

        if branch:
            domain.append(('branch', '=', int(branch)))
        tender_states = ['Contract Awarded']
        # Concatenate the two domains using the + operator
        combined_domain = [('state', 'in', tender_states)] + domain
        tenders = request.env['gntz.tenders'].sudo().search(combined_domain)
        branches = request.env['hr.branches'].sudo().search([])
        return http.request.render('custom_procurement.awarded_tenders_page', {'docs': tenders, 'branches': branches})


class TenderApplicationController(http.Controller):

    @http.route('/apply-tender', type='http', auth="public", website=True)
    def tender_application_form(self, **kw,):
        # Render the application form page
        # tender_id = kw.get('tender_id')
        # Get the tender record based on the ID
        # tender = http.request.env['gntz.tenders'].browse(int(tender_id))
        return http.request.render('custom_procurement.application_form_template')

    @http.route('/submit_application', type='http', auth="public", website=True)
    def submit_application(self, **post):
        # Retrieve form data
        tender_id = post.get('tender_id')
        name = post.get('name')
        email = post.get('email')
        company = post.get('company')
        phone = post.get('phone')
        attachment = request.httprequest.files.get('attachment')
        attachment_name = attachment.filename if attachment else None

        business_licence_attachment = request.httprequest.files.get('business_licence_attachment')
        business_licence_attachment_name = business_licence_attachment.filename if business_licence_attachment else None

        # Handle company profile attachment
        attachment_data = base64.b64encode(attachment.read()) if attachment else None

        # Handle business license attachment
        business_licence_attachment_data = base64.b64encode(business_licence_attachment.read()) if business_licence_attachment else None

        # Save the attachment and other data to your model (tenders.applicants)
        applicants_model = request.env['tenders.applicants']
        applicants_model.create({
            'name': name,
            'email': email,
            'phone': phone,
            'company': company,
            'tender_id': tender_id,
            'attachment': attachment_data,
            'attachment_name': attachment_name,
            'business_licence_attachment': business_licence_attachment_data,
            'business_licence_attachment_name': business_licence_attachment_name,
        })

        # Redirect to a success page or provide feedback to the user
        return http.request.redirect('/application_success')


class AuthenticationCheckController(http.Controller):

    @http.route('/portal_check_logged_in/is_logged_in', type='json', auth='user')
    def check_authentication(self):
        return {'logged_in': bool(request.env.user.id)}


class CustomAuthSignupHome(AuthSignupHome):

    @http.route(['/web/signup'], type='http', auth='public', website=True)
    def web_signup(self, *args, **kw):
        response = super().web_signup(*args, **kw)
        # Process and save the custom fields data here
        # values = {}
        # if 'company_name' in kw:
        #     values['company_name'] = kw.get('company_name')
        # if 'register_license' in kw:
        #     values['register_license'] = kw.get('register_license')
        # request.env['res.partner'].sudo().create(values)
        return response
