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
    name=fields.Char("Name",compute="calcular_name")
    #_website_form_access = True
    date = fields.Datetime("Fecha")
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
    #Lineas a duplicar
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
    tipo_aro_material_id = fields.Many2one(comodel_name="x_material_product", string="Tipo de material del aro.")
    tipo_de_aro = fields.Selection([('Completo','Completo'),("semi_aire", "Semi aire"),('alaire', 'Al aire')], string="Tipo de aro")
    observaciones_aro = fields.Text("Observaciones del aro")
    #medidas hvpd
    medida_h = fields.Float("H")
    medida_v = fields.Float("V")
    medida_d = fields.Float("D")
    medida_p = fields.Float("P")
    observaciones = fields.Text("Observaciones")
   
    color_aro_id = fields.Many2one(comodel_name ="x_product_color", string="Color de aro")
    marca= fields.Char("Marca")
    codigo_disenio= fields.Char("Codigo del diseño")
    valor_esfera_derecho = fields.Selection([("minus","－"),("plus", "＋")], string="Valor esfera derecho")
    valor_cilindro_derecho =fields.Selection([("minus","－"),("plus", "＋")], string="Valor cilindro derecho")
    valor_adiccion_derecho =fields.Selection([("minus","－"),("plus", "＋")], string="Valor addcion derecho")
    prisma_derecho_1 = fields.Selection([("NA","NA"),("U","∇ U"),("D","∆ D"),("O","⊲ O"),("I","⊳ I")], string="Prisma derecho 1")
    prisma_derecho_valor1 = fields.Float("Valor de prisma derecho 1")
    prisma_derecho_2 = fields.Selection([("NA","NA"),("U","∇ U"),("D","∆ D"),("O","⊲ O"),("I","⊳ I")], string="Prisma derecho 2")
    prisma_derecho_valor2 = fields.Float("Valor de prisma derecho 2")
    valor_esfera_izquierdo =fields.Selection([("minus","－"),("plus", "＋")], string="Valor esfera izquierda")
    valor_adicion_izquierdo = fields.Selection([("minus","－"),("plus", "＋")], string="Valor adiccion izquierda")
    valor_cilindro_izquierdo =fields.Selection([("minus","－"),("plus", "＋")], string="Valor cilindro izquierda")
    prisma_izquierda_1 = fields.Selection([("NA","NA"),("U","∇ U"),("D","∆ D"),("O","⊲ O"),("I","⊳ I")], string="Prisma izquierdo 1")
    prisma_izquierda_valor1 = fields.Float("Valor de prisma izquierdo 1")
    prisma_izquierdo_2 = fields.Selection([("NA","NA"),("U","∇ U"),("D","∆ D"),("O","⊲ O"),("I","⊳ I")], string="Prisma izquierdo 2")
    prisma_izquierdo_valor2 = fields.Float("VAlor de prisma izquierdo 2")
    lente_configuracion_ids = fields.One2many(comodel_name="orden_trabajo.configuracion_lente", inverse_name="orden_id",string="Configuraciones de cada lente")
    
    #tipo_lente = fields.Selection([("terminado","TERMINADO"),("digital", 'DIGITAL'), ("convencional","CONVENCIONAL"),("otros","OTROS")], string="Tipo de lente")

   
    tipo_aro = fields.Selection([('semi_aire','Aro semi al aire'),('al_aire','Aro al aire'),('completo','Aro completo')], string="Tipo de aro")
    angulo_panoramico = fields.Float("Angulo panoramico")
    angulo_pantoscopico = fields.Float("Angulo pantoscopico")
    distancia_vertice = fields.Float("Distancia del vertice")
    color_antireflejante_id = fields.Selection([('na',"NA"),("verde","Verde"),("azul","Azul")], string="Color de antireflejante")
    configuracion_avanzada = fields.Boolean("Configuración por ojo")
    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Orden de venta")
    @api.model
    def create(self,values):
        record = super(orden, self).create(values)
        for r in record:
            return r
    def calcular_name(self):
        name = ''
        if self.optica_id:
            name += self.optica_id.name +' '
        name += self.date.strftime('%Y-%m-%d %H:%M:%S')
        self.name = name
    def crear_orden_venta(self):
        for r in self:
            if r.sale_order_id:
                raise ValidationError("Ya tiene una orden de venta vinculada a esta orden de trabajo")
            #iniciando la creacion de la orden de venta
            order = {}
            order["partner_id"] = self.create_uid.partner_id.id
            order["paciente"] = self.paciente
            order["x_orden_status"] = "DIGITADA"
            order["x_sphere_eye_right"] = self.esfera_ojo_derecho
            order["x_cilinder_eye_right"] = self.cilindro_ojo_derecho
            order["x_eje_eye_right"] = self.eje_ojo_derecho
            order["x_prism_eye_right"] = str(self.prisma_derecho_valor1)+"/"+str(self.prisma_derecho_valor2)
            #order["x_prism_eye_right_location"] = self.
            order["x_adition_eye_right"] = self.adiccion_ojo_derecho
            #ojo izquierdo
            order["x_sphere_eye_left"] = self.esfera_ojo_izqueirdo
            order["x_cilinder_eye_left"] = self.cilindro_ojo_izquierdo
            order['x_eje_eye_left'] = self.eje_ojo_izquierdo
            order['x_prism_eye_left'] = str(self.prisma_izquierda_valor1)+"/"+str(self.prisma_izquierdo_valor2)
            order["x_adition_eye_left"] = self.adicion_ojo_izqueirdo
            #order["x_color_transitions"] = self.colo
            order["x_aro_propio"] = self.estado_aro
            order["x_aro"] =  self.codigo_disenio
            order["x_heigh_wafer_eye"] = str(self.oj_derecho_altura_oblea)+"/"+str(self.oj_izquierdo_altura_oblea)
            order["x_heigh_pupilar_eye"] = str(self.oj_derecho_altura_pupilar)+"/"+str(self.oj_izquierdo_altura_pupilar)
            
            #haciendo las lineas de las ordenes
            lineas = []
            for config in self.lente_configuracion_ids:\
                
                lineadic = (0,0,{"product_id":config.producto_template_id.product_variant_id[0].id, 
                            "product_uom_qty": 1,
                            })
                #print(lineadic)
                lineas.append(lineadic)
            if self.color_antireflejante_id == 'verde':
                lineadic = (0,0,{"product_id":124698, 
                            "product_uom_qty": 1,
                            })
                #print(lineadic)
                lineas.append(lineadic)
            if self.color_antireflejante_id == 'azul':
                lineadic = (0,0,{"product_id":122853, 
                            "product_uom_qty": 1,
                            })
                #print(lineadic)
                lineas.append(lineadic)
            order["order_line"] = lineas
            sale_order = self.env["sale.order"].create(order)
            if len(sale_order)>0:
                self.sale_order_id = sale_order.id
            
            
            
    def crearjson(self):
        docs = []
        orden = {}
        orden['date'] = self.date.strftime('%Y-%m-%d %H:%M:%S') if self.date else ''
        orden["paciente"] =  self.paciente if self.paciente else ''
        orden["valor_esfera_derecho"] =self.valor_esfera_derecho
        orden["esfera_ojo_derecho"] = self.esfera_ojo_derecho
        orden["valor_cilindro_derecho"] = self.valor_cilindro_derecho
        orden["cilindro_ojo_derecho"] = self.cilindro_ojo_derecho
        orden["eje_ojo_derecho"] = self.eje_ojo_derecho
        orden["valor_adiccion_derecho"] = self.valor_adiccion_derecho
        orden["adiccion_ojo_derecho"] = self.adiccion_ojo_derecho
        orden["prisma_derecho_1"] = self.prisma_derecho_1
        orden["prisma_derecho_2"] = self.prisma_derecho_2
        orden["valor_esfera_izquierdo"] = self.valor_esfera_izquierdo
        orden["esfera_ojo_izqueirdo"] = self.esfera_ojo_izqueirdo
        orden["valor_cilindro_izquierdo"] = self.valor_cilindro_izquierdo
        orden["cilindro_ojo_izquierdo"] = self.cilindro_ojo_izquierdo
        orden["eje_ojo_izquierdo"] = self.eje_ojo_izquierdo
        orden["valor_adicion_izquierdo"] = self.valor_adicion_izquierdo
        orden["adicion_ojo_izqueirdo"] = self.adicion_ojo_izqueirdo
        orden["prisma_izquierda_1"] = self.prisma_izquierda_1
        orden["prisma_izquierdo_2"] = self.prisma_izquierdo_2
        orden["tipo_orden_id"] = self.tipo_orden_id.name
        orden["oj_derecho_altura_oblea"] = self.oj_derecho_altura_oblea
        orden["oj_derecho_dp_lejos"]=self.oj_derecho_dp_lejos
        orden["oj_derecho_dp_cerca"] = self.oj_derecho_dp_cerca
        orden["oj_izquierdo_altura_oblea"] = self.oj_izquierdo_altura_oblea
        orden["oj_izquierdo_altura_pupilar"]= self.oj_izquierdo_altura_pupilar
        orden["oj_izquierdo_dp_lejos"] = self.oj_izquierdo_dp_lejos
        orden["oj_izquierdo_dp_cerca"] = self.oj_izquierdo_dp_cerca
        orden["marca"] = self.marca
        orden["codigo_disenio"] = self.codigo_disenio
        orden["estado_aro"] = self.estado_aro
        orden["color_aro_id"] = self.color_aro_id.x_name
        orden["medida_h"] = self.medida_h
        orden["medida_v"] = self.medida_v
        orden["medida_d"] = self.medida_d
        orden["medida_p"] = self.medida_p
        orden["tipo_aro"] = self.tipo_aro
        orden["observaciones"] = self.observaciones
        orden["nota_base_uso"] = self.nota_base_uso
        orden["tipo_aro_material_id"] = self.tipo_aro_material_id.x_name
        orden["prisma_derecho_valor2"] = self.prisma_derecho_valor2
        orden["prisma_derecho_valor1"] = self.prisma_derecho_valor1
        orden["prisma_izquierdo_valor2"] = self.prisma_izquierdo_valor2
        orden["prisma_izquierda_valor1"] = self.prisma_izquierda_valor1
        orden['angulo_panoramico'] = self.angulo_panoramico
        orden['angulo_pantoscopico'] = self.angulo_pantoscopico
        orden['distancia_vertice'] = self.distancia_vertice
        orden['color_antireflejante_id'] = self.color_antireflejante_id
        orden["configuracion_avanzada"] = self.configuracion_avanzada
        orden["optica_id"] = self.optica_id.name
        orden["create_uid"] = self.create_uid.partner_id.name if self.create_uid.partner_id else ''
        orden["x_studio_nombre_comercial"] = self.create_uid.partner_id.x_studio_nombre_comercial
        orden["create_date"] = datetime.now()
        orden['_name'] = 'orden_trabajo.orden'
       
        orden['env']=self.env
        configuraciones = []
        for config in self.lente_configuracion_ids:
            config1 = {}
            config1["material_lente_id"] = config.material_lente_id.name
            config1["tratamientos_id"] = config.tratamientos_id.name
            config1['tipo_lente_id'] = config.tipo_lente_id.name
            config1["color_lente_id"] = config.color_lente_id.name
            config1["producto_template_id"] = config.producto_template_id.name
            config1["disenio_lente_id"] = config.disenio_lente_id.name
            config1["tipo"] =  config.tipo
            configuraciones.append(config1)
        orden["lente_configuracion_ids"] = configuraciones
        print("############################")
        #jsondatos = json.dumps(orden)
        return orden
class configuracion_lente(models.Model):
    _name="orden_trabajo.configuracion_lente"
    _description="Esta es la configuracion de lente por ojo"
    tipo = fields.Selection([('izquierda',"Izquierdo"),('derecha',"Derecho"),("unico","Unico")],string="Tipo de configuracion")
    producto_template_id = fields.Many2one(comodel_name="product.template",string='Producto')
    material_lente_id = fields.Many2one(comodel_name ="product.template.attribute.value",string="Material del lente")
    tipo_lente_id = fields.Many2one(comodel_name ='product.template.attribute.value', string='Tipo de lente')
    disenio_lente_id = fields.Many2one(comodel_name ="product.template.attribute.value",string="Disenio el lente")
    tratamientos_id = fields.Many2one(comodel_name ="product.template.attribute.value",string="Tratamientos")
    color_lente_id = fields.Many2one(comodel_name ="product.template.attribute.value", string="Color del lente")
    orden_id = fields.Many2one(comodel_name="orden_trabajo.orden", string="Orden")
    

class tipo_orden(models.Model):
    _name="orden_trabajo.tipo_orden"
    _description = "Tipo de orden de trabajo"
    name = fields.Char("Nombre")
    codigo = fields.Char("Codigo")
    tipo_usuario = fields.Selection([("intern","Interno"),("portal","Portal")], string="Usuario permitido")

class disenio_lente(models.Model):
    _name="orden_trabajo.disenio_lente"
    _description = "Disenio del lente"
    name = fields.Char("Nombre")
class categoria_producto(models.Model):
    _inherit = "product.category"
    visible_sitio = fields.Boolean("Visible en el sitio web")

class product_template_attribute_line(models.Model):
    _inherit="product.template.attribute.line"
    codigo  = fields.Selection([('material','Materiales'),('tipolente','Tipo lente'),('tratamiento','Tratamiento'),('colores','Colores'),('disenio','Diseño'),("validacion","Validación")], string="Codigo")
    

class product_atribute_value(models.Model):
    _inherit="product.attribute.value"
    codigo  = fields.Char("Codigo")

class company_orden(models.Model):
    _inherit="res.company"
    condiciones_servicio = fields.Text("Condiciones de servicio")