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


class Fleet(models.Model):
    _name = 'fleet.vehicle'
    _inherit = 'fleet.vehicle'


    modelo = fields.Char("Año de Fabricación")
    soat = fields.Date("SOAT")
    vigencia_tecnomecanica = fields.Date("Vigencia Tecnomecanica")
    vigencia_del_impuesto = fields.Date("Vigencia del Impuesto")
    accidentes = fields.Char("Cantidad de Accidentes")
    accidentes_motivos = fields.Char("Motivos de los accidentes")
    licencia_conductor = fields.Char("Licencia Conductor")
    licencia_categoria = fields.Char("Licencia Categoria")
    licencia_transito = fields.Char("Licencia Transito")
    vigencia_licencia = fields.Date("Vigencia de Licencia")
    cartype = fields.Selection(
        [
            (1, "Camioneta"),
            (2, "Automóvil"),
            (3, "Moto"),
            (4, "Bicicleta")

        ], "Tipo de vehiculo"
    )
    comments = fields.Text("Comentarios")
    cilindraje = fields.Char("Cilindraje")
    motor = fields.Char("Motor")
