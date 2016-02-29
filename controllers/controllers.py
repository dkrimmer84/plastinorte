# -*- coding: utf-8 -*-
from openerp import http

# class Plastinorte(http.Controller):
#     @http.route('/plastinorte/plastinorte/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/plastinorte/plastinorte/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('plastinorte.listing', {
#             'root': '/plastinorte/plastinorte',
#             'objects': http.request.env['plastinorte.plastinorte'].search([]),
#         })

#     @http.route('/plastinorte/plastinorte/objects/<model("plastinorte.plastinorte"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('plastinorte.object', {
#             'object': obj
#         })