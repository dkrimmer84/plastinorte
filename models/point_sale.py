###############################################################################
#                                                                             #
# Copyright (C) 2016  Dominic Krimmer                                         #
#                     Luis Alfredo da Silva (luis.adasilvaf@gmail.com)        #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU Affero General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Affero General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################
import logging
import time

import openerp.addons.decimal_precision as dp
from odoo import tools, models, SUPERUSER_ID
from odoo import fields, api
from odoo.tools import float_is_zero
from odoo.tools.translate import _
from odoo.exceptions import UserError
from datetime import datetime

from uuid import getnode as get_mac
from odoo import api, fields as Fields
import locale
from odoo.tools.misc import formatLang
from odoo.osv import osv
from odoo.http import request
_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _name = "pos.order"
    _inherit = "pos.order"

    origin = fields.Many2one('pos.order', 'Origen')

    

    @api.multi
    def refund(self):
        request.session['copy_origin'] = True
        res = super(PosOrder, self).refund()

        return res

    @api.multi
    def copy(self, default=None):
        copy_origin = request.session.get('copy_origin')
        if copy_origin:
            default.update({
                'origin' : self.id
            })
        request.session['copy_origin'] = False

        default = dict(default or {})
        return super(PosOrder, self).copy(default)


'''class pos_make_payment(osv.osv_memory):
    _inherit = 'pos.make.payment'

    @api.model
    def default_get(self, vals):   

        result = super(pos_make_payment, self).default_get(vals)

        order_id = self.env.context.get('active_id')
        if order_id:
            order_origin = self.env['pos.order'].sudo().browse(order_id).origin.id
        
            if order_origin:
                _statement_ids = self.env['pos.order'].sudo().browse(order_origin).statement_ids[0].id

                if _statement_ids:
                    metds_payments = self.env['account.bank.statement.line'].sudo().browse(_statement_ids).journal_id.id

                    if metds_payments:
                        result.update({
                            'journal_id' : metds_payments
                        })

        return result
'''
