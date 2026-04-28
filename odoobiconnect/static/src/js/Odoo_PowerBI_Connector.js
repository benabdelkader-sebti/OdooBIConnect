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
            notification.add(_t("تم نسخ رمز الدخول! افتح الملف وقم بلصقه في خانة Access_Token"), {
                type: "success",
            });
            
            const templateUrl = "/odoobiconnect/static/src/pbit/odoo_universal_connection_power_bi_data.pbit";
            browser.location.href = templateUrl;
        } else {
            notification.add(_t("يرجى توليد رمز الدخول أولاً"), { type: "danger" });
        }
    }
};