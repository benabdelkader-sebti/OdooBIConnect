# -*- coding: utf-8 -*-
import jwt
import secrets
from datetime import datetime, timedelta
from odoo import models, fields, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    jwt_secret = fields.Char(string="Secret JWT")
    generated_access_token = fields.Char(string="Access Token", readonly=True)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('odoobiconnect.jwt_secret', self.jwt_secret)
        self.env['ir.config_parameter'].sudo().set_param('odoobiconnect.last_token', self.generated_access_token)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            jwt_secret=self.env['ir.config_parameter'].sudo().get_param('odoobiconnect.jwt_secret'),
            generated_access_token=self.env['ir.config_parameter'].sudo().get_param('odoobiconnect.last_token'),
        )
        return res

    def action_generate_jwt_secret(self):
        # 1. توليد السر والتوكن
        new_secret = secrets.token_urlsafe(32)
        payload = {
            'user_id': self.env.user.id,
            'exp': datetime.utcnow() + timedelta(days=365)
        }
        token = jwt.encode(payload, new_secret, algorithm='HS256')
        new_token = token.decode('utf-8') if isinstance(token, bytes) else token

        # 2. الحفظ الفوري في قاعدة البيانات
        self.env['ir.config_parameter'].sudo().set_param('odoobiconnect.jwt_secret', new_secret)
        self.env['ir.config_parameter'].sudo().set_param('odoobiconnect.last_token', new_token)

        # 3. تحديث الحقول
        self.jwt_secret = new_secret
        self.generated_access_token = new_token

        # 4. الحل الجذري: إرسال أمر للمتصفح بإعادة تحميل الصفحة (Reload) بدلاً من البحث عن XML ID
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def _generate_display_token(self):
        secret = self.jwt_secret or self.env['ir.config_parameter'].sudo().get_param('odoobiconnect.jwt_secret')
        if secret:
            payload = {
                'user_id': self.env.user.id,
                'exp': datetime.utcnow() + timedelta(days=365)
            }
            token = jwt.encode(payload, secret, algorithm='HS256')
            self.generated_access_token = token.decode('utf-8') if isinstance(token, bytes) else token

    def action_connect_to_powerbi(self):
        self._generate_display_token()
        self.set_values()       
        return {
            'type': 'ir.actions.act_url',
            'url': '/odoobiconnect/static/src/pbit/odoo_universal_connection_power_bi_data.pbit',
            'target': 'new',
        }