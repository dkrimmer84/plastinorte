# -*- coding: utf-8 -*-
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
from openerp import tools, models, SUPERUSER_ID
from openerp import fields, api
from openerp.tools import float_is_zero
from openerp.tools.translate import _
from openerp.exceptions import UserError
from datetime import datetime

from uuid import getnode as get_mac
from openerp import api, fields as Fields
import locale
from openerp.tools.misc import formatLang
from openerp.osv import osv

_logger = logging.getLogger(__name__)



"""class PosAccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"

    base_tax = fields.Float('Base Tax')"""

class PosOrder(models.Model):
    _name = "pos.order"
    _inherit = "pos.order"

    origin = fields.Many2one('pos.order', 'Origen')

    
    def refund(self, cr, uid, ids, context=None):
        """Create a copy of order  for refund order"""
        clone_list = []
        line_obj = self.pool.get('pos.order.line')
        
        for order in self.browse(cr, uid, ids, context=context):
            current_session_ids = self.pool.get('pos.session').search(cr, uid, [
                ('state', '!=', 'closed'),
                ('user_id', '=', uid)], context=context)
            if not current_session_ids:
                raise UserError(_('To return product(s), you need to open a session that will be used to register the refund.'))

            clone_id = self.copy(cr, uid, order.id, {
                'name': order.name + ' REFUND', # not used, name forced by create
                'session_id': current_session_ids[0],
                'date_order': time.strftime('%Y-%m-%d %H:%M:%S'),
                'origin' : order.id,
            }, context=context)
            clone_list.append(clone_id)

        for clone in self.browse(cr, uid, clone_list, context=context):
            for order_line in clone.lines:
                line_obj.write(cr, uid, [order_line.id], {
                    'qty': -order_line.qty
                }, context=context)

        abs = {
            'name': _('Return Products'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pos.order',
            'res_id':clone_list[0],
            'view_id': False,
            'context':context,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        return abs


class pos_make_payment(osv.osv_memory):
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




