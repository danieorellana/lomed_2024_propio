from odoo import api, fields, models,_

class orden_trabajo_parametro(models.Model):
    _name="orden_trabajo.parametro"
    _descripcion = "Parametros a remplazar en el codigo a ejecutar"
    name = fields.Char("Nombre")
    nombreclave = fields.Char("Nombre clave")
    llave = fields.Char("Palabra clave in codigo")
    