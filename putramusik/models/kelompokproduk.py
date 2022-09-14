from odoo import api, fields, models


class KelompokProduk(models.Model):
    _name = 'putramusik.kelompokproduk'
    _description = 'New Description'

    name = fields.Selection([
        ('elektrik', 'Elektrik'),
        ('non elektrik', 'Non Elektrik'),
        ('gitar elektrik', 'Gitar Elektrik'),
        ('gitar non elektrik', 'Gitar Non Elektrik'),
    ], string='Nama Kelompok')

    kode_kelompok = fields.Char(string='Kode Kelompok')

    @api.onchange('name')
    def _onchange_kode_kelompok(self):
        if self.name == 'elektrik':
            self.kode_kelompok = 'ELK01'
        elif self.name == 'non elektrik':
            self.kode_kelompok = 'NELK01'
        elif self.name == 'gitar elektrik':
            self.kode_kelompok = 'GELK01'
        elif self.name == 'gitar NON elektrik':
            self.kode_kelompok = 'GNELK01'

    kode_rak = fields.Char(string='Kode Rak')
    produk_ids = fields.One2many(comodel_name='putramusik.produk',
                                inverse_name='kelompokproduk_id',
                                string='Daftar Produk')
    jml_item = fields.Char(compute='_compute_jml_item', string='Jml Item')

    @api.depends('produk_ids')
    def _compute_jml_item(self):
        for record in self:
            a = self.env['putramusik.produk'].search([('kelompokproduk_id', '=', record.id)]).mapped('name')
            b = len(a)
            record.jml_item = b
            record.daftar = a
    
    daftar = fields.Char(string='Daftar isi')