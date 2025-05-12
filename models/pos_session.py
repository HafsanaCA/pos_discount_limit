# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PosSession(models.Model):
    _inherit = 'pos.session'

    allow_discount_control = fields.Boolean(string="Enable Discount Control", compute="_compute_max_discount_amount", store=True)
    max_allowed_discount = fields.Float(string="Maximum Discount Amount")

    @api.depends('config_id')
    def _compute_max_discount_amount(self):
        param = self.env['ir.config_parameter'].sudo()
        discount_control_enabled = param.get_param('pos_discount_limit.enable_discount_control', 'False') == 'True'
        max_discount_value = float(param.get_param('pos_discount_limit.max_discount_amount', '0'))
        for session in self:
            session.allow_discount_control = discount_control_enabled
            session.max_allowed_discount = max_discount_value if discount_control_enabled else 0.0

    @api.model
    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result += ['allow_discount_control', 'max_allowed_discount']
        return result
