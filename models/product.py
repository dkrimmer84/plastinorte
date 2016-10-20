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


class Consecutive(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    change_category = fields.Boolean(string="Cambiar referencia interna?", default=True)

    def onchange_category(self, cr, uid, ids, catid=False, change_cat=False, context=True):
        """
        This function takes the chosen category ID and checks if this
        category has a prefix given. If yes, he will look in the database
        for the next consecutive.
        If there is no prefix given, then nothing happens
        If it is a totally new prefix, the product will have number 1 as first
        number
        @param catid: category ID which is chosen by the user in the interface
        @return: object

        """
        # First check if Change is allowed by change_cat
        if catid and change_cat:
            obj = self.pool.get('product.category')
            ids = obj.search(cr, uid, [('id', '=', catid)])
            for rec in obj.browse(cr, uid, ids):
                # If there is no prefix given in the product config, do nothing
                # Otherwise, go for it:
                if rec.consecutive is not False:
                    cr.execute("SELECT \
                               default_code FROM product_product \
                               WHERE \
                               default_code LIKE %s \
                               ORDER BY substring(default_code, '\d+')::int \
                               DESC NULLS FIRST LIMIT %s",
                               (rec.consecutive+'%', 1))

                    result = cr.dictfetchall()

                    # If there was a result then go ahead:
                    # Otherwise set if to false in order to create a
                    # totally new consecutive number (1)
                    last_consecutive = result[0]['default_code'] \
                        if cr.rowcount > 0 \
                        else False

                    if last_consecutive:
                        new_consecutive = self.increase_consecutive(
                            last_consecutive
                        )
                    else:
                        # If there was no result because there was no
                        # consecutive so far with this prefix,
                        # we create a new one with numer 1
                        if '-' in rec.consecutive:
                            new_consecutive = rec.consecutive + '-1'
                        else:
                            return False

                    return {'value': {'default_code': new_consecutive}}

    @staticmethod
    def increase_consecutive(last_consecutive=False):
        """
        Here we go: We are increasing the consecutive by +1
        @param last_consecutive:
        @return:
        """
        if last_consecutive:
            if '-' in last_consecutive:
                sep = string.split(last_consecutive, '-')
                if len(sep) > 0:
                    return str(sep[0]) + '-' + \
                           str(sep[1]) + '-' + \
                           str((int(sep[2])+1))
        return False


class PrefixCategory(models.Model):
    """
    Model that adds a new field: consecutive prefix
    This field makes is easy to generate consecutives in the product
    template more easily
    """
    _name = 'product.category'
    _inherit = 'product.category'

    consecutive = fields.Char("Consecutivo Prefijo")


class ProductName(models.Model):
    """
    Many people have the bad habit in writing everyting in uppercase (HATE IT!)
    Here we are making product names more beautiful:
    e.j. MY PRODUCT NAME => My Product Name
    """
    _name = 'product.template'
    _inherit = 'product.template'

    @api.onchange('name')
    def onchange_product_name(self):
        self.name = self.name.title() if self.name else ''
