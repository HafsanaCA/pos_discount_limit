# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class PosDiscountDeductionController(http.Controller):
    @http.route('/pos/calculate_maximum_discount_limit', type='json', auth='user')
    def calculate_maximum_discount_limit(self, session_id, deducted_discount):
        pos_session = request.env['pos.session'].browse(session_id)
        if pos_session and pos_session.max_allowed_discount is not None:
            pos_session.max_allowed_discount -= deducted_discount
        return True

