from odoo import models, api, fields,_
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta, date


class resequence_config(models.Model):
    _name="resequence.config"
    _description="Resequence Config"
    _order="id desc"
    name= fields.Char(string="Nombre",default="Menu de resecuenciacion")
    planned_action = fields.Many2one(comodel_name="ir.cron",string="Acción programada")
    email_to_notify = fields.Char(string="Email to notify")
    last_updated_secuence = fields.Html(string="Ultima actualización")
    update_log = fields.Html(string="Registro de cambios")
    def create_planned_action(self):
        if self.planned_action:
            self.planned_action.unlink()
        anio = datetime.now().year
        dic = {
            'name': 'Reiniciar secuencias DTE',
            'model_id': self.env['ir.model']._get_id('resequence.config'),
            'state': 'code',
            'code': 'model.resecuence_all()',
            'interval_number': 12,
            'interval_type': 'months',
            'active': True, 
            'nextcall': (date(anio, 12, 31) + timedelta(days=1)).strftime('%Y-%m-%d') + " 04:59:59",
        }
        self.planned_action = self.env['ir.cron'].create(dic)
    def resecuence_all(self):
        result = []
        documentos = []
        if self.env['odoosv.fiscal.document'].fields_get().get('sequencia_id'):
            documentos += self.env['odoosv.fiscal.document'].search([('sequencia_id.number_next_actual', '>', 0),('name','!=',False)])
        if self.env['odoosv.fiscal.document'].fields_get().get('secuencia_dedicada'):
            documentos += self.env['odoosv.fiscal.document'].search([('secuencia_dedicada', '>', 0),('name','!=',False)])
        for r in documentos:
            if self.env['odoosv.fiscal.document'].fields_get().get('sequencia_id'):
                    result += r.set_sequence()
            if self.env['odoosv.fiscal.document'].fields_get().get('secuencia_dedicada'):
                result += r.set_dedicate_sequence()
        texto = ""
        _logger.info(result)
        for r in result:
            texto += "<p>Caja: "+r['caja']+" Documento: "+r['name']+" Anterior: "+str(r['anterior'])+" Actual: "+str(r['actual'])+"</p><br>"
        configuracion = self.search([], limit=1)
        if  configuracion:
            configuracion.last_updated_secuence = texto
            configuracion.update_log = texto.replace("<br>","").replace("<p>","").replace("</p>","") + configuracion.update_log if configuracion.update_log else ''
            configuracion.send_email()
        return result
    
    def send_email(self):
        template = []
        template= self.env.ref("sv_restart_secuence.resequencia_email_template")
        if len(template) >0:
            template.send_mail(self.id,force_send=True)
        