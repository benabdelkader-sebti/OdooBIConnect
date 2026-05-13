/** @odoo-module **/

import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";

const copyAndDownloadAction = async (env, action) => {
    const token = action.params.access_token;
    const url = action.params.download_url;

    try {
        await browser.navigator.clipboard.writeText(token);
        
        env.services.notification.add(
            "The token has been successfully copied! You can paste it into Power BI.", 
            { type: "success", title: "Copied" }
        );
    } catch (error) {
        console.error("Error copying token :", error);
        env.services.notification.add(
            "Unable to copy the token automatically.", 
            { type: "Danger" }
        );
    }

    browser.location.href = url;
};

registry.category("actions").add("odoobiconnect.action_copy_and_download", copyAndDownloadAction);