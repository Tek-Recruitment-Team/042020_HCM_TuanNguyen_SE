# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger()

class Ticket(models.Model):
    _name = 'showing.ticket'
    _order = 'id desc'

    showing_id = fields.Many2one('room.showing', string="Showing", required=True)
    seat_id = fields.Many2one('room.seat', string="Seat", required=True)