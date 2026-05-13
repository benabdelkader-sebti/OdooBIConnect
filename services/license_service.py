import requests
from .exceptions import LicenseInvalid

class LicenseService:

    def __init__(self, env):
        self.env = env

    def validate(self):

        key = self.env['ir.config_parameter'].sudo().get_param(
            "odoobiconnect.license_key"
        )

        if not key:
            raise LicenseInvalid("License key missing")

        response = requests.get(
            "https://license.odoobiconnect.com/validate",
            params={"key": key}
        )

        if response.status_code != 200:
            raise LicenseInvalid("License validation failed")

        data = response.json()

        if not data.get("valid"):
            raise LicenseInvalid("Invalid license")
        return True
