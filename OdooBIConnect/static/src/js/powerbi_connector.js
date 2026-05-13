/** @odoo-module **/

import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";

export const PowerBIConnector = {
    async onConnectClick(token, templateUrl) {
       
        await browser.navigator.clipboard.writeText(token);
        
        
        alert("تم نسخ التوكن بنجاح! سيتم الآن تحميل قالب Power BI.");
        
        
        browser.location.href = templateUrl;
    }
};