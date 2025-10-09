from odoo import fields, models, api, _


class account_move_inherit_sv_fe(models.Model):
    _inherit="account.move"
    
    def get_emisor(self):
        for r in self:
            res = super(r, account_move_inherit_sv_fe).get_emisor()
            if res:
                if r.caja_id:
                    r['codEstableMH']= r.caja_id.cod_estable_mh
                    r['codEstable']=r.caja_id.cod_stable
                    r['codPuntoVentaMH']=r.caja_id.cod_punto_venta_mh
                    r['codPuntoVenta']=r.caja_id.cod_punto_venta
        return res
    