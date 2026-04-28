/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

export const PowerBIConnectorAction = {
    async executeConnect() {
        const notification = useService("notification");        
        const tokenElement = document.querySelector(".o_powerbi_token_input");
        const token = tokenElement ? tokenElement.value : "";

        if (token) {            
            await browser.navigator.clipboard.writeText(token);            
            notification.add(_t("The access code has been copied! Open the file and paste it into the Access_Token field."), {
                type: "success",
            });
            
            const templateUrl = "/odoobiconnect/static/src/pbit/odoo_universal_connection_power_bi_data.pbit";
            browser.location.href = templateUrl;
        } else {
            notification.add(_t("Access_Token field. Please generate the access token first."), { type: "danger" });
        }
    }
};