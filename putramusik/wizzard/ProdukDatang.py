from odoo import api, fields, models


class ProdukDatang(models.TransientModel):
    _name = 'putramusik.produkdatang'

    produk_id = fields.Many2one(
        comodel_name='putramusik.produk',
        string='Nama Produk',
        required=True)


    jumlah = fields.Integer(
        string='Jumlah',
        required=False)

    def button_produk_datang(self):
        for rec in self:
            self.env['putramusik.produk'] \
                .search([('id', '=', rec.produk_id.id)]) \
                .write({'stok': rec.produk_id.stok + rec.jumlah})