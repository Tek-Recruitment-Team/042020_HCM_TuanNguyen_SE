# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger()

class TransactionPayment(models.Model):
    _name = 'transaction.payment'
    _order = 'id desc'
