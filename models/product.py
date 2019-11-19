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
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    override_default_code = fields.Boolean(string="Create internal reference automatically?", default=True)
    
    """
    Many people have the bad habit in writing everyting in uppercase (HATE IT!)
    Here we are making product names more beautiful:
    e.j. MY PRODUCT NAME => My Product Name
    """
    @api.multi
    def write(self, vals):
        if vals.get('name'):
            vals['name'] = vals['name'].title()
        
        set_default_code = False

        if vals.get('categ_id'):
            if self.override_default_code:
                if 'override_default_code' in vals:
                    if vals.get('override_default_code'):
                        set_default_code = True
                else:
                    set_default_code = True
        
        if vals.get('override_default_code'):
            set_default_code = True

        if set_default_code:
            if not self.categ_id.sequence_id:
                raise ValidationError(_("This category haven't sequence assigned! "
                                        "You can't override code, please uncheck the above field."))

            if vals.get('categ_id'):
                category = self.env['product.category'].search([('id', '=', vals.get('categ_id'))], limit=1)
            else:
                category = self.categ_id
            
            vals['default_code'] = category.sequence_id.next_by_id()

        return super(ProductTemplate, self).write(vals)
    
    @api.onchange('categ_id', 'override_default_code')
    def _onchange_category(self):
        if self.override_default_code:
            if self.categ_id:
                self.default_code = self.categ_id.sequence_id.prefix


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        rec = super(ProductProduct, self).create(vals)
        
        if rec.name:
            rec.name = rec.name.title()

        if rec.override_default_code:
            if not rec.categ_id.sequence_id:
                raise ValidationError(_("This category haven't sequence assigned! "
                                        "You can't override code, please uncheck the above field."))
            rec.default_code = rec.categ_id.sequence_id.next_by_id()
        
        return rec
    
    @api.multi
    def write(self, vals):
        if vals.get('name'):
            vals['name'] = vals['name'].title()
        
        set_default_code = False

        if vals.get('categ_id'):
            if self.override_default_code:
                if 'override_default_code' in vals:
                    if vals.get('override_default_code'):
                        set_default_code = True
                else:
                    set_default_code = True
            elif vals.get('override_default_code'):
                set_default_code = True

        if set_default_code:
            if not self.categ_id.sequence_id:
                raise ValidationError(_("This category haven't sequence assigned! "
                                        "You can't override code, please uncheck the above field."))
            vals['default_code'] = self.categ_id.sequence_id.next_by_id()
        
        return super(ProductProduct, self).write(vals)

    # Internal reference field has to be unique,
    # therefore a constraint will validate it:
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
