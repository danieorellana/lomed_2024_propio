# -*- coding: utf-8 -*-
{
    'name': "Firmador SV",

    'summary': """
        Este modulo contiene las funcionalidad de firmar on documento desde odoo
       """,

    'description': """
       Este modulo contiene las funcionalidad de firmar on documento desde odoo
    """,

    'author': "RG Ingenieros",
    'website': "https://rgingenierossv.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '18.0',

    # any module necessary for this one to work correctly
    'depends': ['sv_fe'],

    # always loaded
    'data': ['views/ambiente.xml'],
    'demo': [],
    #'external_dependencies': {
    #    'python': ['python-jose'],
    #},
}
