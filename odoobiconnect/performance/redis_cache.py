import redis
import logging
from odoo import http

_logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self):
        # جلب إعدادات الاتصال من بارامترات النظام أو استخدام الافتراضي
        self.host = 'localhost'
        self.port = 6379
        self.enabled = True
        try:
            self.client = redis.Redis(host=self.host, port=self.port, decode_responses=True)
        except Exception as e:
            self.enabled = False
            _logger.error(f"Failed to connect to Redis: {e}")

    def get(self, key):
        if not self.enabled: return None
        try:
            return self.client.get(key)
        except Exception:
            return None

    def set(self, key, value, expiry=3600):
        if not self.enabled: return
        try:
            self.client.setex(key, expiry, value)
        except Exception as e:
            _logger.warning(f"Redis Set Error: {e}")