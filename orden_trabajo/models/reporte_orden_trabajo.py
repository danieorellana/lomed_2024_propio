from odoo import api, models, fields, _
class ReportClassName(models.AbstractModel):
  _name = 'orden_trabajo.reporte_orden_trabajo'

  @api.model
  def render_html(self, docids, data=None):
    docargs = {
    'doc_ids': self.ids,
    'doc_model': self.model,
    'data': data,
    }
    return self.env['report'].render('orden_trabajo.reporte_orden_trabajo', docargs)