# -*- coding: utf-8 -*-
import json
import datetime
import logging
import jwt
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

class OdooPowerBIConnector(http.Controller):

    @http.route('/odata/data/<string:model_name>', type='http', auth='public', methods=['GET', 'OPTIONS'], cors='*', csrf=False)
    def get_odoo_data(self, model_name, **kwargs):

        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Content-Type': 'application/json'
        }

        if request.httprequest.method == 'OPTIONS':
            return Response(json.dumps({"status": "ready"}), status=200, headers=headers)

        try:
            param_obj = request.env['ir.config_parameter'].sudo()
            secret_key = param_obj.get_param('odoobiconnect.jwt_secret')
            
            client_token = kwargs.get('token')
            if not secret_key:
                _logger.error("❌ Error: Not set. odoobiconnect.jwt_secret in System Parameters")
                return Response(json.dumps({"error": "Configuration Missing"}), status=500, headers=headers)

            if not client_token:
                _logger.warning("🛑 Login Rejected: The token is missing from the link.")
                return Response(json.dumps({"error": "Token Required"}), status=403, headers=headers)

            try:
                jwt.decode(client_token, secret_key, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                _logger.warning("🛑 Login Rejected: The token has expired.")
                return Response(json.dumps({"error": "Token Expired"}), status=403, headers=headers)
            except jwt.InvalidTokenError:
                _logger.warning("🛑 Login Rejected: The token is literally invalid.")
                return Response(json.dumps({"error": "Invalid Token Signature"}), status=403, headers=headers)

            formatted_model = model_name.replace('_', '.')
            
            if formatted_model not in request.env:
                _logger.error("❌ Model %s does not exist in the Odoo database", formatted_model)
                return Response(json.dumps({"error": f"Model {formatted_model} not found"}), status=404, headers=headers)

            records = request.env[formatted_model].sudo().search_read([], limit=5000)

            processed_data = []
            for record in records:
                row = {}
                for k, v in record.items():
                    if isinstance(v, (datetime.date, datetime.datetime)):
                        row[k] = v.isoformat()
                    elif isinstance(v, tuple) and len(v) == 2:
                        row[k] = v[1]
                    elif v is False:
                        row[k] = None
                    else:
                        row[k] = v
                processed_data.append(row)

            _logger.info("✅ %s record from model %s was successfully sent", len(processed_data), formatted_model)
            return Response(json.dumps({"value": processed_data}, default=str), status=200, headers=headers)

        except Exception as e:
            _logger.error("🔥 Read the following instructions: %s", str(e))
            return Response(json.dumps({"error": "Internal Server Error", "details": str(e)}), status=500, headers=headers)