from odoo import fields, models, api
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64
import xml.etree.ElementTree as ET
from jose import jws
import logging
_logger = logging.getLogger(__name__)
class ambiente_inherit(models.Model):
    _inherit="sv_fe.ambiente"
    certificado = fields.Binary(string="Certificado")
    certificado_name = fields.Char(string="Nombre de certificado")
    def firmardoc(self, json):
        llave = self.get_private_key()
        jws_token = jws.sign(
            payload=json.encode(),
            key=llave,
            algorithm='RS512'  # RSA con SHA-256
        )
        _logger.info("info")
        print("firma")
        #print(jws_token)
        return jws_token
    def get_certificado_xml(self):
        decoded_bytes = base64.b64decode(self.certificado)
        decoded_string = decoded_bytes.decode('ISO-8859-1')
        tree = ET.fromstring(decoded_string)
        return tree
    
    def get_private_key(self, salt = None):
        cert = self.get_certificado_xml()
        #encoded_key = cert.findall('.//encodied').text.strip()
        for child in cert.findall('.//encodied'):
            encoded_key = child.text.strip()
        key_material = base64.b64decode(encoded_key)

        # 2. Cargar la clave privada
        private_key = serialization.load_der_private_key(
        key_material,
        password=None,
        backend=default_backend()
        )
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        return pem_key

        
