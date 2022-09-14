# -*- coding: utf-8 -*-
# from odoo import http


# class Putramusik(http.Controller):
#     @http.route('/putramusik/putramusik', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/putramusik/putramusik/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('putramusik.listing', {
#             'root': '/putramusik/putramusik',
#             'objects': http.request.env['putramusik.putramusik'].search([]),
#         })

#     @http.route('/putramusik/putramusik/objects/<model("putramusik.putramusik"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('putramusik.object', {
#             'object': obj
#         })
