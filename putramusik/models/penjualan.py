from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class Penjualan(models.Model):
    _name = 'putramusik.penjualan'
    _description = 'New Description'

    name = fields.Char(string='No. Nota')
    nama_pembeli = fields.Char(string='Nama Pembeli')
    tgl_penjualan = fields.Datetime(
        string='Tanggal Transaksi',
        default=fields.Datetime.now())
    total_bayar = fields.Integer(
        string='Total Pembayaran',
        compute='_compute_totalbayar')
    detailpenjualan_ids = fields.One2many(
        comodel_name='putramusik.detailpenjualan',
        inverse_name='penjualan_id',
        string='Detail Penjualan')

    state=fields.Selection(selection=[('draft','Draft'),('confirm','Confirm'),('cancel','Cancel'),('done','Done')],default='draft')
    id_member=fields.Integer(string='member id')

    @api.depends('detailpenjualan_ids')
    def _compute_totalbayar(self):
        for line in self:
            result = sum(self.env['putramusik.detailpenjualan'].search(
                [('penjualan_id', '=', line.id)]).mapped('subtotal'))
            line.total_bayar = result

    def write(self, vals):
        for line in self:
          data_asli = self.env['putramusik.detailpenjualan'].search([('penjualan_id', '=', line.id)])
          print(data_asli)

          for data in data_asli:
              print(str(data.produk_id.name) + " " + str(data.qty) + ' ' + str(data.produk_id.stok))
              data.produk_id.stok += data.qty
      
        line = super(Penjualan, self).write(vals)
      
        for line in self:
          data_setelah_edit = self.env['putramusik.detailpenjualan'].search([('penjualan_id', '=', line.id)])
          print(data_asli)
          print(data_setelah_edit)

          for data_baru in data_setelah_edit:
              if data_baru in data_asli:
                  print(data_baru.produk_id.name + " " + str(data_baru.qty) + ' ' + str(data_baru.produk_id.stok))
                  data_baru.produk_id.stok -= data_baru.qty
              else:
                  pass

        return line

    def action_confirm (self):
        self.state='confirm'
    def action_done (self):
        self.state='done'
    def action_cancel (self):
        self.state='cancel'
    def action_draft (self):
        self.state='draft'


class DetailPenjualan(models.Model):
    _name = 'putramusik.detailpenjualan'
    _description = 'Detail'

    name = fields.Char(string='Nama')
    penjualan_id = fields.Many2one(
        comodel_name='putramusik.penjualan',
        string='Detail Penjualan')
    produk_id = fields.Many2one(
        comodel_name='putramusik.produk',
        string='List Produk')
    harga_satuan = fields.Integer(
        string='Harga Satuan',
        onchange='_onchange_produk_id')
    qty = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Subtotal')

    @api.depends('harga_satuan', 'qty')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * line.harga_satuan

    @api.onchange('produk_id')
    def _onchange_produk_id(self):
        if self.produk_id.harga_jual:
            self.harga_satuan = self.produk_id.harga_jual

    @api.model
    def create(self, vals):
        line = super(DetailPenjualan, self).create(vals)
        if line.qty:
            self.env['putramusik.produk'].search(
                [('id', '=', line.produk_id.id)]
            ).write({'stok': line.produk_id.stok - line.qty})
        return line

    def unlink(self):
        if self.detailpenjualan_ids:
            penjualan = []
            for line in self:
                penjualan = self.env['putramusik.detailpenjualan'].search(
                    [('penjualan_id', '=', line.id)])
                print(penjualan)

            for ob in penjualan:
                print(ob.produk_id.name + ' ' + str(ob.qty))
                ob.produk_id.stok += ob.qty
        return super(Penjualan, self).unlink()

    sql_constraints = [
    ('no_nota_unik', 'unique (name)', 'Nomor Nota tidak boleh sama!')
    ]         

    @api.constrains('qty')
    def check_quantity(self):
        for line in self:
            if line.qty < 1:
                raise ValidationError('Jumlah pembelian harus minimal 1, silahkan input dengan benar!')
            elif line.produk_id.stok < line.qty:
                raise ValidationError('Stok yang tersedia tidak mencukupi.')   