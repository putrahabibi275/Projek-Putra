from odoo import api, fields, models


class Produk(models.Model):
    _name = 'putramusik.produk'
    _description = 'New Description'

    name = fields.Char(string='Nama Produk')
    harga_beli = fields.Integer(string='Harga Modal', required=True)
    harga_jual = fields.Integer(string='Harga Jual', required=True)
    kelompokproduk_id = fields.Many2one(comodel_name='putramusik.kelompokproduk',
                                        string='Kelompok Produk',
                                        ondelete='cascade')

    supplier_id = fields.Many2many(comodel_name='putramusik.supplier', string='Supplier')
    stok = fields.Integer(string='Stok')

                                        