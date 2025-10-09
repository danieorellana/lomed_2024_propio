from odoo import fields, models, api, _


class account_move_inherit_sv_fe(models.Model):
    _inherit="account.move"
    
    def get_emisor(self):
        for r in self:
            res = super(account_move_inherit_sv_fe, r).get_emisor()
            if res:
                if r.caja_id:
                    res['codEstableMH']= r.caja_id.cod_estable_mh
                    res['codEstable']=r.caja_id.cod_stable
                    res['codPuntoVentaMH']=r.caja_id.cod_punto_venta_mh
                    res['codPuntoVenta']=r.caja_id.cod_punto_venta
        return res
    