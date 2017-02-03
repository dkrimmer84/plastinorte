# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016  Dominic Krimmer                                         #
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

# Extended Product Template
from openerp import models, fields, api, exceptions
import string

from openerp.addons.account.wizard.pos_box import CashBox
import logging
_logger = logging.getLogger(__name__)

class inherit_PosBoxOut(CashBox):
    _name = 'cash.box.out'
    _inherit = 'cash.box.out'

    product_expenses = fields.Many2one('product.product', 'Expenses', required=True)

    @api.model
    def create(self, values):   

        res = super(inherit_PosBoxOut, self).create(values)


        if res:
            model_hr_expenses = self.env['hr.expense']
            model_hr_expenses.create({
                'name' : res.name,
                'product_id' : res.product_expenses.id,
                'unit_amount' : res.amount,
                'quantity' : 1,
                'employee_id' : self.env.uid,
                'tax_ids' : res.product_expenses.supplier_taxes_id,
                'payment_mode' : 'company_account',
                'bank_journal_id' : 5,
                'state' : 'submit'
                })
            pass
        
        return res  

