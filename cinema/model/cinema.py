# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger()

class Cinema(models.Model):
    _name = 'cinema.cinema'
    _order = 'id desc'

    manager_id = fields.Many2one('hr.employee', string="Manager", required=True)