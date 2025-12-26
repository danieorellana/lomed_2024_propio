from odoo import models, api, fields, _

class odoosv_fiscal_document(models.Model):
    _inherit="odoosv.fiscal.document"
    def set_sequence(self, start=0):
        response = []
        for r in self:
            if r.sequencia_id and r.sequencia_id.number_next_actual > 0:
                dic = {'name':r.name,'anterior':r.sequencia_id.number_next_actual,'actual':start, 'caja':r.caja_id.name if r.caja_id else 'No asignada'}
                r.sequencia_id.number_next_actual = start
                response.append(dic)
        return response
            
    def set_dedicate_sequence(self, start=0):
        response = []
        for r in self:
            if r.secuencia_dedicada > 0:
               dic = {'name':r.name,'anterior':r.secuencia_dedicada,'actual':start, 'caja':r.caja_id.name if r.caja_id else 'No asignada'}
               r.secuencia_dedicada = start
               response.append(dic)
        return response
                
