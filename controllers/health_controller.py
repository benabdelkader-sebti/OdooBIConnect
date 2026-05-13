from odoo import http
from odoo.http import request
import json

class HealthController(http.Controller):

    @http.route('/odoobiconnect/health', auth='public', type='http')
    def health(self):
        return request.make_response(
            json.dumps({"status": "ok"}),
            headers=[('Content-Type', 'application/json')]
        )
