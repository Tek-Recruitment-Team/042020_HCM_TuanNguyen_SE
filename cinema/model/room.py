# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger()


class Room(models.Model):
    _name = 'cinema.room'
    _order = 'id desc'

    cinema_id = fields.Many2one('cinema.cinema', string="Cinema", required=True)