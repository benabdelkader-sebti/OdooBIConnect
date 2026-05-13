import requests
from odoo import models, fields

class PowerBIConnector(models.Model):
    _name = 'powerbi.connector'
    _description = 'Power BI API Connector'

    def action_force_refresh(self):
        """استدعاء Power BI API لتحديث البيانات فوراً"""
        workspace_id = "YOUR_WORKSPACE_ID"
        dataset_id = "YOUR_DATASET_ID"
        token = "YOUR_AZURE_AD_TOKEN"
        
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
        headers = {'Authorization': f'Bearer {token}'}
        
        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 202:
                return {'type': 'ir.actions.client', 'tag': 'display_notification', 
                        'params': {'title': 'Success', 'message': 'Refresh Started!', 'type': 'success'}}
        except Exception as e:
            return False