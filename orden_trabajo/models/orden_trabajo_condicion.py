from odoo import api, fields, models,_
from odoo.tools.safe_eval import safe_eval

class orden_trabajo_condicion(models.Model):
    _name="orden_trabajo.condicion"
    _description ="Condicion a evaluar por campo"
    name=fields.Char("Nombre")
    evento = fields.Selection([('onchange',"Al cambiar"),('required',"Requerido"),("setrequired","Asignar requeridos")
                               ], string="Evento", default="onchange")
    codigoejecutar = fields.Text("Codigo a ejecutar")
    mensajeerror = fields.Text("Mensaje  al dar error")
    parametros_ids = fields.Many2many(comodel_name ="orden_trabajo.parametro", string="Parametros")
    usadependencias = fields.Boolean("Usa dependencias")
    def ejecutarvalidacion(self, vals):
        env = {}
        env["self"] = self
        codigoejecutar= self.codigoejecutar
        valor = vals.get('valor')
        dependencias = vals.get('dependencias')
        codigoejecutar = self.codigoejecutar.replace('${VALOR}',valor)
        for para in self.parametros_ids:
            #llave = self.parametros_ids.filtered(lambda m: m.nombreclave == para.get('nombreclave'))
            valor1 = dependencias.get(para.nombreclave)
            if valor1:
                codigoejecutar = codigoejecutar.replace(para.llave,valor1)
        print(codigoejecutar)
        eval = safe_eval(codigoejecutar,env,mode='exec', nocopy=True)
        print(env.get('result'))
        if env.get('result'):
            result = {'result':'ok'}
        else:
            m = env.get('mensaje')
            mensaje = ''
            if m:
                mensaje = m
            else:
                mensaje = self.mensajeerror
            result = {'result':'no','mensaje': mensaje}
        return result