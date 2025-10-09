from odoo import fields, models, api, _

class odoosv_caja_inherit(models.Model):
    _inherit="odoosv.caja"
    cod_punto_venta = fields.Char("Codigo punto de venta")
    cod_punto_venta_mh = fields.Char("Codigo punto de venta MH")
    cod_estable_mh = fields.Char("Codigo del establecimiento MH")
    cod_stable = fields.Char("Codigo establecimiento")
    