# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#
##############################################################################
import base64
import json
import requests
import logging
import time
from datetime import datetime
from collections import OrderedDict
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval
_logger = logging.getLogger(__name__)


class orden(models.Model):
    _name="orden_trabajo.orden"
    _description="Orden para hacer un proceso de produccion"
    #_website_form_access = True
    date = fields.Date("Fecha")
    create_date = fields.Datetime("Fecha de creacion")
    #create_uid = fields.Many2one(comodel_name ='res.users', string='Creado por')
    optica_id = fields.Many2one(comodel_name ="odoosv.caja",string="Optica")
    paciente = fields.Char("Nombre paciente")
    #apartado de receta
    #valor de la esfera
    esfera_ojo_derecho = fields.Float(string="Esfera Ojo derecho")
    esfera_ojo_izqueirdo = fields.Float(string = "Esfera Ojo izqueirdo")
    cilindro_ojo_derecho = fields.Float(string = "Cilindro ojo derecho")
    cilindro_ojo_izquierdo = fields.Float(string="Cilindro ojo izquierda")
    eje_ojo_derecho = fields.Float(string="Eje ojo derecho")
    eje_ojo_izquierdo = fields.Float(string = "Eje ojo izquierdo")
    adiccion_ojo_derecho = fields.Float(string="Adiccion ojo derecho")
    adicion_ojo_izqueirdo = fields.Float(string="Adicion ojo izquierdo")
    tipo_orden_id = fields.Many2one(comodel_name="orden_trabajo.tipo_orden",string="Tipo de orden")
    producto_template_id = fields.Many2one(comodel_name="product.template",string='Producto')
    nota_base_uso = fields.Char("Base en uso")
    #MEDIDAS
    #ojo derecho
    oj_derecho_altura_oblea = fields.Float(string="Ojo derecho altura oblea")
    oj_derecho_altura_pupilar = fields.Float(string="Ojo derecho alura pupilar")
    oj_derecho_dp_lejos = fields.Float(string="Ojo derecho dp lejos")
    oj_derecho_dp_cerca = fields.Float(string="Ojo derecho dp cerca")
    #ojo izquierdo
    oj_izquierdo_altura_oblea = fields.Float(string="Ojo derecho altura oblea")
    oj_izquierdo_altura_pupilar = fields.Float(string="Ojo derecho alura pupilar")
    oj_izquierdo_dp_lejos = fields.Float(string="Ojo derecho dp lejos")
    oj_izquierdo_dp_cerca = fields.Float(string="Ojo derecho dp cerca")
    estado_aro=fields.Selection([('nuevo',"Nuevo"),("usado",'Usado')], string="Estado del aro")
    tipo_de_aro = fields.Selection([('Completo','Completo'),("semi_aire", "Semi aire"),('alaire', 'Al aire')], string="Tipo de aro")
    observaciones_aro = fields.Text("Observaciones del aro")
    #medidas hvpd
    medida_h = fields.Float("H")
    medida_v = fields.Float("V")
    medida_d = fields.Float("D")
    medida_p = fields.Float("P")
    observaciones = fields.Text("Observaciones")
    color_lente_id = fields.Many2one(comodel_name ="product.template.attribute.value", string="Color el lente")
    color_aro_id = fields.Many2one(comodel_name ="x_product_color", string="Color de aro")
    marca= fields.Char("Marca")
    codigo_disenio= fields.Char("Codigo del diseño")
    valor_esfera_derecho = fields.Selection([("minus","－"),("plus", "＋")], string="Valor esfera derecho")
    valor_cilindro_derecho =fields.Selection([("minus","－"),("plus", "＋")], string="Valor cilindro derecho")
    valor_adiccion_derecho =fields.Selection([("minus","－"),("plus", "＋")], string="Valor addcion derecho")
    prisma_derecho_1 = fields.Selection([("NA","NA"),("U","∇ U"),("D","∆ D"),("O","⊲ O"),("I","⊳ I")], string="Prisma derecho 1")
    prisma_derecho_2 = fields.Selection([("NA","NA"),("U","∇ U"),("D","∆ D"),("O","⊲ O"),("I","⊳ I")], string="Prisma derecho 2")
    valor_esfera_izquierdo =fields.Selection([("minus","－"),("plus", "＋")], string="Valor esfera izquierda")
    valor_adicion_izquierdo = fields.Selection([("minus","－"),("plus", "＋")], string="Valor adiccion izquierda")
    valor_cilindro_izquierdo =fields.Selection([("minus","－"),("plus", "＋")], string="Valor cilindro izquierda")
    prisma_izquierda_1 = fields.Selection([("NA","NA"),("U","∇ U"),("D","∆ D"),("O","⊲ O"),("I","⊳ I")], string="Prisma izquierdo 1")
    prisma_izquierdo_2 = fields.Selection([("NA","NA"),("U","∇ U"),("D","∆ D"),("O","⊲ O"),("I","⊳ I")], string="Prisma izquierdo 2")
    material_lente_id = fields.Many2one(comodel_name ="product.template.attribute.value",string="Material del lente")
    tratamientos_id = fields.Many2one(comodel_name ="product.template.attribute.value",string="Tratamientos")
    #tipo_lente = fields.Selection([("terminado","TERMINADO"),("digital", 'DIGITAL'), ("convencional","CONVENCIONAL"),("otros","OTROS")], string="Tipo de lente")
    tipo_lente_id = fields.Many2one(comodel_name ='product.template.attribute.value', string='Tipo de lente')
    disenio_lente_id = fields.Many2one(comodel_name ="product.template.attribute.value",string="Disenio el lente")
    tipo_aro = fields.Selection([('semi_aire','Aro semi al aire'),('al_aire','Aro al aire'),('completo','Aro completo')], string="Tipo de aro")
    angulo_panoramico = fields.Float("Angulo panoramico")
    angulo_pantoscopico = fields.Float("Angulo pantoscopico")
    distancia_vertice = fields.Float("Distancia del vertice")
    @api.model
    def create(self,values):
        record = super(orden, self).create(values)
        for r in record:
            return r
    


class tipo_orden(models.Model):
    _name="orden_trabajo.tipo_orden"
    _description = "Tipo de orden de trabajo"
    name = fields.Char("Nombre")
    codigo = fields.Char("Codigo")

class disenio_lente(models.Model):
    _name="orden_trabajo.disenio_lente"
    _description = "Disenio del lente"
    name = fields.Char("Nombre")
class categoria_producto(models.Model):
    _inherit = "product.category"
    visible_sitio = fields.Boolean("Visible en el sitio web")

class product_template_attribute_line(models.Model):
    _inherit="product.template.attribute.line"
    codigo  = fields.Selection([('material','Materiales'),('tipolente','Tipo lente'),('tratamiento','Tratamiento'),('colores','Colores'),('disenio','Diseño')], string="Codigo")