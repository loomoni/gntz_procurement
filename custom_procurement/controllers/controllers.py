from addons.website.controllers.main import Website
from odoo import http
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
