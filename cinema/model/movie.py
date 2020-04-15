# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger()

class Movie(models.Model):
    _name = 'movie.movie'
    _order = 'id desc'

