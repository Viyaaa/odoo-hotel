from odoo import api, fields, models


class Room(models.Model):
    _name = 'hotel.room'
    _description = 'List of Hotel Rooms'

    name = fields.Char(string='Room ID', required=True)
    type = fields.Char(string='Room Type', required=True)
    stock = fields.Integer(string='Stock', required=True)
    description = fields.Char(string='Description')
    price = fields.Integer(string='Price')
