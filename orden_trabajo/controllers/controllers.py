# -*- coding: utf-8 -*-
# from odoo import http
import logging
import pprint
import werkzeug
import json
import requests
import datetime
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect


class PortalAccount(http.Controller):
    @http.route('/orden_trabajo', auth='user',  website=True)
    def new_recordx(self, **kw):
        datos = {}
        # hacien
        datos['tipo_ordenes'] = request.env['orden_trabajo.tipo_orden'].sudo().search([])
        #datos["material_lente"] = request.env['x_material_product'].sudo().search([])
        datos["material_lente"] = []
        #datos["tipo_lente"] = request.env['x_type_lens'].sudo().search([])
        datos["tipo_lente"] =[]
        #disenio_lente
        #producto=
        datos["prismas"] = [{"value":"NA","content":"NA"},{"value":"U","content":"∇ U"},{"value":"D",'content':"∆ D"},{"value":"O","content":"⊲ O"},{"value":"I","content":"⊳ I"}]
        #datos["prismas"] = prismas
        #datos["tratamientos"] = request.env['x_treatment_base'].sudo().search([])
        datos["tratamientos"] = []
        datos["coloraro"] = request.env['x_product_color'].sudo().search([])
        datos["color"] =[]
        datos["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        datos["productos"] = request.env['product.template'].sudo().search([("categ_id.visible_sitio","=",True)])
        #datos["disenios"] = request.env["orden_trabajo.disenio_lente"].sudo().search([])
        datos["disenios"] = []
        #datos["tipo_aros"] = [{"value":"semi_aire","content":"Aro semi al aire"},{"value":"al_aire","content":"Aro al aire"},{"value":"completo","content":"Aro completo"}]
        datos["tipo_aros"] = [{'value':'semi_aire','content':'Aro semi al aire'},{'value':'al_aire','content':'Aro al aire'},{'value':'completo','content':'Aro completo'}]
        return request.render('orden_trabajo.formulario',datos)
    
    @http.route('/orden_trabajo/success', auth='user', website=True)
    def success(self, **kwargs):
        return request.render('orden_trabajo.success_orden_trabajo')
    
    @http.route('/orden_trabajo/get_materiales', type='json', auth='public')
    def get_materiales(self, **post):
        product_line_atri = request.env['product.template.attribute.line'].search([('product_tmpl_id','=',int(post.get('id')))])
        print(product_line_atri)
        resultado={}
        resultado['materiales'] = []
        #materiales
        materiale = []
        materiales = product_line_atri.filtered(lambda r: r.codigo == 'material')
        for item in materiales.product_template_value_ids:
            dic = {}
            dic['name'] = item.name
            dic['id'] = item.id
            materiale.append(dic)
        resultado['materiales'] = materiale
        #tipo lente
        tipolente = []
        tipolentes = product_line_atri.filtered(lambda r: r.codigo == 'tipolente')
        for item in tipolentes.product_template_value_ids:
            dic = {}
            dic['name'] = item.name
            dic['id'] = item.id
            tipolente.append(dic)
        resultado['tipolente'] = tipolente
        #disenios
        tratamiento = []
        tratamientos = product_line_atri.filtered(lambda r: r.codigo == 'tratamiento')
        for item in tratamientos.product_template_value_ids:
            dic = {}
            dic['name'] = item.name
            dic['id'] = item.id
            tratamiento.append(dic)
        resultado['tratamientos'] = tratamiento
        #colores
        colore = []
        colores = product_line_atri.filtered(lambda r: r.codigo == 'colores')
        for item in colores.product_template_value_ids:
            dic = {}
            dic['name'] = item.name
            dic['id'] = item.id
            colore.append(dic)
        resultado['colores'] = colore
        disenio = []
        disenios = product_line_atri.filtered(lambda r: r.codigo == 'disenio')
        for item in disenios.product_template_value_ids:
            dic = {}
            dic['name'] = item.name
            dic['id'] = item.id
            disenio.append(dic)
        resultado['disenios'] = disenio
        #lineas_material = producto.attribute_line_ids.filtered(lambda r: r.codigo == 'material')
        #print(lineas_material)
        return json.dumps(resultado)
    
    @http.route('/orden_trabajo/crear', type='http', auth='user', website=True)
    def crear(self, **post):
        print(post)
        orden = {}
        orden['date'] = post.get("date")
        orden["paciente"] = post.get("paciente")
        orden["valor_esfera_derecho"] = post.get("valor_esfera_derecho")
        orden["esfera_ojo_derecho"] = post.get("esfera_ojo_derecho")
        orden["valor_cilindro_derecho"] = post.get("valor_cilindro_derecho")
        orden["cilindro_ojo_derecho"] = post.get("cilindro_ojo_derecho")
        orden["eje_ojo_derecho"] = post.get("eje_ojo_derecho")
        orden["valor_adiccion_derecho"] = post.get("valor_adiccion_derecho")
        orden["adiccion_ojo_derecho"] = post.get("adiccion_ojo_derecho")
        orden["prisma_derecho_1"] = post.get("prisma_derecho_1")
        orden["prisma_derecho_2"] = post.get("prisma_derecho_2")
        orden["valor_esfera_izquierdo"] = post.get("valor_esfera_izquierdo")
        orden["esfera_ojo_izqueirdo"] = post.get("esfera_ojo_izqueirdo")
        orden["valor_cilindro_izquierdo"] = post.get("valor_cilindro_izquierdo")
        orden["cilindro_ojo_izquierdo"] = post.get("cilindro_ojo_izquierdo")
        orden["eje_ojo_izquierdo"] = post.get("eje_ojo_izquierdo")
        orden["valor_adicion_izquierdo"] = post.get("valor_adicion_izquierdo")
        orden["adicion_ojo_izqueirdo"] = post.get("adicion_ojo_izqueirdo")
        orden["prisma_izquierda_1"] = post.get("prisma_izquierda_1")
        orden["prisma_izquierdo_2"] = post.get("prisma_izquierdo_2")
        orden["tipo_orden_id"] = post.get("tipo_orden_id")
        orden["material_lente_id"] = post.get("material_lente_id")
        orden["tratamientos_id"] = post.get("tratamientos_id")
        orden['tipo_lente_id'] = post.get("tipo_lente_id")
        orden["color_lente_id"] = post.get("color_lente_id")
        orden["oj_derecho_altura_oblea"] = post.get("oj_derecho_altura_oblea")
        orden["oj_derecho_dp_lejos"]=post.get("oj_derecho_dp_lejos")
        orden["oj_derecho_dp_cerca"] = post.get("oj_derecho_dp_cerca")
        orden["oj_izquierdo_altura_oblea"] = post.get("oj_izquierdo_altura_oblea")
        orden["oj_izquierdo_altura_pupilar"]= post.get("oj_izquierdo_altura_pupilar")
        orden["oj_izquierdo_dp_lejos"] = post.get("oj_izquierdo_dp_lejos")
        orden["oj_izquierdo_dp_cerca"] = post.get("oj_izquierdo_dp_cerca")
        orden["marca"] = post.get("marca")
        orden["codigo_disenio"] = post.get("codigo_disenio")
        orden["estado_aro"] = post.get("estado_aro")
        orden["color_aro_id"] = post.get("color_aro_id")
        orden["medida_h"] = post.get("medida_h")
        orden["medida_v"] = post.get("medida_v")
        orden["medida_d"] = post.get("medida_d")
        orden["medida_p"] = post.get("medida_p")
        orden["tipo_aro"] = post.get("tipo_aro")
        orden["observaciones"] = post.get("observaciones")
        orden["nota_base_uso"] = post.get("nota_base_uso")
        orden["disenio_lente_id"] = post.get("disenio_lente_id")
        orden["producto_template_id"] = post.get("producto_template_id")
        orden['angulo_panoramico'] = post.get('angulo_panoramico')
        orden['angulo_pantoscopico'] = post.get('angulo_pantoscopico')
        orden['distancia_vertice'] = post.get('distancia_vertice')
        user = request.env["res.users"].sudo().browse(request.session.uid)
        if user.caja_id:
            orden["optica_id"] = user.caja_id.id
       
        orden_c = request.env["orden_trabajo.orden"].sudo().create(orden)
        vals = {'orden': orden_c}

        return request.render('orden_trabajo.success_orden_trabajo',vals)
    
