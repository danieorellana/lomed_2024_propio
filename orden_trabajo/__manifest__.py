# -*- coding: utf-8 -*-
{
    'name': "orden_trabajo",

    'summary': """Crea ordenes de trabajo por el sistio web""",

    'description': """Crea ordenes de trabajo por el sitio""",

    'author': "Rgingenieros",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0',

    # any module necessary for this one to work correctly
    'depends': ['website','product','sv_accounting','sv_caja',],

    # always loaded
    'data': [
       
        'security/ir.model.access.csv',
        'data/data.xml',
        'static/src/xml/orden_trabajo.xml',
        'views/views.xml',
        
    ],
     'images': [
        'static/src/img/d.png',
        'static/src/img/h.png',
        'static/src/img/p.png',
        'static/src/img/v.png',
    ],
     'assets': {
    'web.assets_frontend': [
        'orden_trabajo/static/src/js/validations.js',
        # other files or globs as needed
    ]
    },
     'qweb': [
         
         ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
