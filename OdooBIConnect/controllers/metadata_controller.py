from odoo import http
from odoo.http import request
import json

class MetadataController(http.Controller):

    @http.route('/odoobiconnect/metadata/<string:model>',
                auth='user', type='http')
    def metadata(self, model):

        if model not in request.env:
            return {"error": "Invalid model"}

        fields = request.env[model]._fields
        data = {}

        for name, field in fields.items():
            data[name] = {
                "type": field.type,
                "string": field.string
            }

        return request.make_response(
            json.dumps(data),
            headers=[('Content-Type', 'application/json')]
        )
