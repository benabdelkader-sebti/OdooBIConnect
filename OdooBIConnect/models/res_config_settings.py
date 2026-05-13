# -*- coding: utf-8 -*-
import jwt
import secrets
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    jwt_secret = fields.Char(
        string="Clé secrète JWT",
        config_parameter='odoobiconnect.jwt_secret',
        help="Generated to sign Access_Token tokens"
    )
   
    generated_access_token = fields.Text(
        string="Access Token (Copiable)",
        readonly=True,
        help="Copiez ce code et collez-le dans Power BI"
    )

    def action_generate_jwt_secret(self):
        """توليد السر وحفظه في النظام"""
        new_secret = secrets.token_urlsafe(32)
        self.env['ir.config_parameter'].sudo().set_param('odoobiconnect.jwt_secret', new_secret)
        self.jwt_secret = new_secret
        
        self._generate_display_token()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('JWT key generated. You can now log in.'),
                'type': 'success',
                'sticky': False,
            }
        }

    def _generate_display_token(self):
        """دالة داخلية لتوليد JWT لعرضه للمستخدم"""
        secret = self.env['ir.config_parameter'].sudo().get_param('odoobiconnect.jwt_secret')
        if secret:
            payload = {
                'user_id': self.env.user.id,
                'exp': datetime.utcnow() + timedelta(days=365)
            }
            token = jwt.encode(payload, secret, algorithm='HS256')
            if isinstance(token, bytes):
                token = token.decode('utf-8')
            self.generated_access_token = token

    def action_connect_to_powerbi(self):
        """توليد التوكن وإرساله لواجهة العميل لنسخه وتحميل القالب"""
        self._generate_display_token()
        if not self.generated_access_token:
            raise UserError(_("Please generate a secret key first."))

        return {
            'type': 'ir.actions.client',
            'tag': 'odoobiconnect.action_copy_and_download', # اسم الإجراء الذي سنعرفه في JS
            'params': {
                'access_token': self.generated_access_token,
                'download_url': '/odoobiconnect/static/src/pbit/odoo_universal_connection_power_bi_data.pbit',
            }
        }

    @api.model
    def check_license_frozen(self):
        return True