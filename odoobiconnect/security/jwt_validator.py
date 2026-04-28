import jwt
import logging
from odoo import http, exceptions
from odoo.http import request

_logger = logging.getLogger(__name__)

class JWTValidator:
    @staticmethod
    def validate_token(token):
        # جلب المفتاح السري من إعدادات Odoo
        secret_key = request.env['ir.config_parameter'].sudo().get_param('odoobiconnect.jwt_secret')
        
        if not secret_key:
            _logger.error("JWT Secret Key missing in System Parameters")
            raise exceptions.AccessDenied("Missing Configuration")

        try:
            # فك تشفير الرمز
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            user = request.env['res.users'].sudo().browse(user_id)
            if not user.exists():
                raise exceptions.AccessDenied("User not found")
            
            return user
        except Exception as e:
            _logger.error(f"JWT Error: {str(e)}")
            raise exceptions.AccessDenied("Invalid Token")

def require_jwt(func):
    """Decorator لحماية المسارات"""
    def wrapper(*args, **kwargs):
        auth_header = request.httprequest.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise exceptions.AccessDenied("Authorization Required")
        
        token = auth_header.split(" ")[1]
        user = JWTValidator.validate_token(token)
        
        # تحديث البيئة لتطبيق صلاحيات المستخدم والـ RLS
        request.update_env(user=user.id)
        return func(*args, **kwargs)
    return wrapper