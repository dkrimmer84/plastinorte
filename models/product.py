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

import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    override_default_code = fields.Boolean(string="Create internal reference automatically?", default=True)

    _sql_constraints = [
        ('default_unique',
         'UNIQUE(default_code)',
         "La Referencia interna debe ser única!")
    ]

    
    @api.model
    def create(self, vals):
        if vals['override_default_code']:
            if 'default_code' not in vals or vals['default_code'] == '/':
                categ_id = vals.get("categ_id")
                categ = sequence = False
                if categ_id:
                    # Created as a product.product
                    categ = self.env['product.category'].browse(categ_id)
                if categ:
                    sequence = categ.sequence_id
                if not sequence:
                    raise UserError('No sequence')
                vals['default_code'] = sequence.next_by_id()
        return super(ProductTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        for product in self:
            if vals.get('default_code', '') == '':
                if vals.get('override_default_code', '') or self.override_default_code:
                    category_id = vals.get('categ_id', product.categ_id.id)
                    category = self.env['product.category'].browse(category_id)
                    sequence = category.sequence_id
                    if not sequence:
                        raise UserError('No sequence')
                    ref = sequence.next_by_id()
                    vals['default_code'] = ref
            super(ProductTemplate, product).write(vals)
        return True

    @api.onchange('categ_id', 'override_default_code')
    def _onchange_category(self):
        self.default_code = False


class ProductProduct(models.Model):
    _inherit = 'product.product'

    _sql_constraints = [
        ('default_unique',
         'UNIQUE(default_code)',
         "La Referencia interna debe ser única!")
    ]
  


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
    
    @api.multi
    def unlink(self):
        sequence = self.sequence_id
        res = super(ProductCategory, self).unlink()

        if res:
            sequence.unlink()

        return res

    @api.model
    def create_sequence_for_categories(self):
        categories = self.env['product.category'].search([('sequence_id', '=', False)])

        if categories:
            for cat in categories:
                cat.sequence_id = cat._create_sequence()
