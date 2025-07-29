from odoo import api, models, fields, _

class error_register(models.Model):
    _name="orden_trabajo.error_register"
    _description = "Registro de errores al momento de validar la orden de trabajo."
    create_date = fields.Datetime(string="Fecha de creacion")
    description = fields.Text("Registro")
    condiciones_id = fields.Many2one(comodel_name ="orden_trabajo.condicion", string="Condicion")