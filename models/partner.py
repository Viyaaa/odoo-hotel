from odoo import api, fields, models


class Partner(models.Model):
    _name = 'hotel.partner'
    _description = 'New Description'

    name = fields.Char(string='Name')
    type = fields.Selection(string='Type', selection=[(
        'customer', 'Customer'), ('employee', 'Employee'), ])
