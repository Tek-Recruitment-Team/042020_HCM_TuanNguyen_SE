# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger()

class Showing(models.Model):
    _name = 'room.showing'
    _order = 'id desc'

    room_id = fields.Many2one('cinema.room', string="Room", required=True)
    movie_id = fields.Many2one('movie.movie', string="Movie", required=True)

