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

import string
import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    override_default_code = fields.Boolean(string="Cambiar referencia interna?", default=True)

    """
    Assigning secuence number on create if needed
    """
    @api.model
    def create(self, vals):
        rec = super(ProductTemplate, self).create(vals)
        if rec.name:
            rec.name = rec.name.title()

        if rec.override_default_code:
            rec.default_code = rec.categ_id.sequence_id.next_by_id()
        
        return rec
    
    """
    Many people have the bad habit in writing everyting in uppercase (HATE IT!)
    Here we are making product names more beautiful:
    e.j. MY PRODUCT NAME => My Product Name
    """
    @api.multi
    def write(self, vals):
        if vals.get('name'):
            vals['name'] = vals['name'].title()
        return super(ProductTemplate, self).write(vals)


class ProductCategory(models.Model):
    _inherit = 'product.category'

    sequence_id = fields.Many2one("ir.sequence", readonly=True, copy=False)

    @api.model
    def create(self, vals):
        rec = super(ProductCategory, self).create(vals)
        if not rec.sequence_id:
            rec.sequence_id = rec._create_sequence()

        return rec
    
    @api.model
    def _create_sequence(self):
        return self.env['ir.sequence'].sudo().create({
            'name': 'Product Category ' + self.name,
            'implementation': 'no_gap',
            'padding': 4,
            'number_increment': 1,
            'use_date_range': False
        })

''' TODO: Check this constrains

    @api.constrains('check_default_code', 'helper_check_default_code')
    def _check_default_code(self):
        if self.change_category:
            # raise exceptions.ValidationError(self.check_default_code)
            if self.check_default_code != self.helper_check_default_code:
                raise exceptions.ValidationError(
                    "Pusiste una referencia que no es conforme a la categoria."
                    " Por favor, escoja una categoría y la referencia se genera"
                    " automático.")
'''


class CheckUniqueRef(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    def onchange_category(self, cr, uid, ids, catid=False, change_cat=False, context=True):
        product_template_model = self.pool.get('product.template')
        return  product_template_model.onchange_category(cr, uid, ids, catid, change_cat , context)


    # Internal reference field has to be unique,
    # therefore a constraint will validate it:
    _sql_constraints = [
        ('default_unique',
         'UNIQUE(default_code)',
         "La Referencia interna debe ser única!")
    ]
