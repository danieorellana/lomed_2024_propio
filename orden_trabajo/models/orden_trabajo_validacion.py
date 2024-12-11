from odoo import api, fields, models,_
import sys
import traceback

class orden_trabajo_validacion(models.Model):
    _name = "orden_trabajo.validacion"
    _description = "Valida campos del  sitio web"
    
    name = fields.Char("Nombre")
    nombrecampo = fields.Char("Nombre del campo")
    identificador =fields.Char("Identificador")
    condiciones_ids = fields.Many2many(comodel_name ="orden_trabajo.condicion", string="Condiciones")
    
    def validarcampo(self,values):
        if len(self.condiciones_ids)> 0:
            valido = 'ok'
            mensaje = ''
            condiciones = self.condiciones_ids.filtered(lambda x: x.evento == values.get("evento"))
            for condicion in condiciones:
                try:
                    result = condicion.ejecutarvalidacion(values)
                    if result['result'] != 'ok':
                        valido = 'no'
                        mensaje += result['mensaje']
                except  Exception as e:
                    print(e)
                    info = ''
                    for i in sys.exc_info():
                        info += str(i)+'\n'
                    print(info)
                    print(str(e.args) + '\n' + info + '\n'+sys.argv[0]+'\n'+sys.argv[1] +'\n'+traceback.format_exc())
            result = {'result':valido,'mensaje':mensaje}
                    
        else:
            result = {'result':'ok'}
        return result