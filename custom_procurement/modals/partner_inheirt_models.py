from odoo import fields, models


class ResPartnerCustom(models.Model):
    _inherit = 'res.partner'

    company_name = fields.Char(string='Company Name')
    # register_licenses = fields.Char(string='Register License')
