# -*- coding: utf-8 -*-
{
    'name': "Reinicio sv_fe secuencias",

    'summary': """
     Reinicia las secuencias de los documentos de sv_fe""",

    'description': """
     Reinicia las secuencias de los documentos de sv_fe
    """,

    'author': "RG Ingenieros",
    'website': "https://rgingenieros.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sv_fe'],

    # always loaded
    'data': [
        "data/data.xml",
        'views/resequence_config.xml',
        'views/mail_template.xml',
        "security/ir.model.access.csv",

    ],
    # only loaded in demonstration mode
    'demo': [],
}
