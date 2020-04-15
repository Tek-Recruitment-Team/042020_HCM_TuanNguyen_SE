# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger()


class Seat(models.Model):
    _name = 'room.seat'
    _order = 'id desc'

    room_id = fields.Many2one('cinema.room', string="Room", required=True)