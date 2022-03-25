from openerp.exceptions import ValidationError
from odoo import api, fields, models
from datetime import datetime


class RoomOrder(models.Model):
    _name = 'hotel.room_order'
    _description = 'Room Orders'

    name = fields.Char(string='Order ID')
    date_order = fields.Datetime('Order Date', default=fields.Datetime.now())
    date_checkin = fields.Date(
        string='Check In', required=True, default=fields.Datetime.now())
    date_checkout = fields.Date(
        string='Check Out', required=True, default=fields.Datetime.now())

    days_count = fields.Integer(
        string="Days Count", compute='_compute_days_count')

    @api.depends('date_checkin', 'date_checkout')
    def _compute_days_count(self):
        for record in self:
            record.days_count = int(
                ((record.date_checkout - record.date_checkin)).days)

    orderroomdetail_ids = fields.One2many(
        comodel_name='hotel.order_room_detail', inverse_name='order_room_id', string='Room Order')

    orderadditionaldetail_ids = fields.One2many(
        comodel_name='hotel.order_additional_detail', inverse_name='order_additional_id', string='Additional Order')

    price = fields.Integer(string='Total Price',
                           compute='_compute_price', store=True)

    @api.depends('orderroomdetail_ids')
    def _compute_price(self):
        for record in self:
            room = sum(self.env['hotel.order_room_detail'].search(
                [('order_room_id', '=', record.id)]).mapped('price'))
            additional = sum(self.env['hotel.order_additional_detail'].search(
                [('order_additional_id', '=', record.id)]).mapped('price'))
            record.price = ((room + additional) * record.days_count)

    payment = fields.Selection(string='Payment Type', selection=[(
        'credit card', 'Credit Card'), ('online payment', 'Online Payment'), ('cash', 'Cash',), ('debit card', 'Debit Card')])

    # customer personal information
    cust_name = fields.Char(string='Customer Name')
    phone_num = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')

    


class OrderRoomDetail(models.Model):
    _name = 'hotel.order_room_detail'
    _description = 'Room Order Detail'

    name = fields.Char(string='Name')
    order_room_id = fields.Many2one(
        comodel_name='hotel.room_order', string='Order')
    room_id = fields.Many2one(comodel_name='hotel.room', string='Room')
    qty = fields.Integer(string='Quantity', required=True)

    price_per_unit = fields.Integer(
        compute='_compute_price_per_unit', string='Price per Unit')

    @ api.depends('room_id')
    def _compute_price_per_unit(self):
        for record in self:
            record.price_per_unit = record.room_id.price

    price = fields.Integer(compute='_compute_price', string='price')

    @ api.depends('qty', 'price_per_unit')
    def _compute_price(self):
        for record in self:
            record.price = record.price_per_unit * record.qty

    # Decrease room stock
    @api.model
    def create(self, vals):
        record = super(OrderRoomDetail, self).create(vals)
        if record.qty:
            self.env['hotel.room'].search(
                [('id', '=', record.room_id.id)]).write({'stock': record.room_id.stock - record.qty})


class OrderAdditionalDetail(models.Model):
    _name = 'hotel.order_additional_detail'
    _description = 'Additional Order Detail'

    name = fields.Char(string='Name')
    order_additional_id = fields.Many2one(
        comodel_name='hotel.room_order', string='Order')
    additional_id = fields.Many2one(
        comodel_name='hotel.additional', string='Additional')
    qty = fields.Integer(string='Quantity', required=True)

    price_per_unit = fields.Integer(
        compute='_compute_price_per_unit', string='Price per Unit')

    @ api.depends('additional_id')
    def _compute_price_per_unit(self):
        for record in self:
            record.price_per_unit = record.additional_id.price

    price = fields.Integer(compute='_compute_price', string='price')

    @ api.depends('qty', 'price_per_unit')
    def _compute_price(self):
        for record in self:
            record.price = record.price_per_unit * record.qty
