# 🚀 OdooBIConnect

**The Ultimate OData Bridge between Odoo and Microsoft Power BI.**

---

## 📖 Overview
**OdooBIConnect** is a high-performance tool designed to expose Odoo data as an OData feed. This allows Power BI to fetch records directly without complex SQL queries or middle-ware. It handles security via **JWT (JSON Web Tokens)** and supports all Odoo versions.

---

## ✨ Key Features
* **🔒 Automated Security:** Generates a unique JWT Secret automatically upon installation.
* **📡 OData v4 Protocol:** Standardized data format recognized natively by Power BI.
* **🔗 Smart Relation Mapping:** Automatically extracts both **ID** and **Name** for Many2One fields.
* **🌐 Multi-DB Support:** Handles environments with multiple databases using the `db` parameter.

---

## 🛠️ Installation & Best Practices
1. **Download** the branch corresponding to your Odoo version.
2. **Place** the `odoobiconnect` folder into your Odoo `addons` path.
3. **Install Dependencies:** ```bash
   pip install pyjwt.  

---

[!TIP]Recommended Database Naming: For optimal compatibility and to avoid connection issues in multi-db environments, it is highly recommended to name your Odoo database data1.

---

📊 Power BI Usage Guide

1. Construct the URL

The module generates a dynamic URL. Ensure it includes your database name:
http://[YOUR_DOMAIN]:8069/odata/data/[MODEL_NAME]?token=[YOUR_TOKEN]&db=data1

2. Connect in Power BI

Open Power BI Desktop -> Get Data -> OData Feed.

Paste your URL.

CRITICAL: When prompted for credentials, select Anonymous.

---

📋 Compatibility Matrix

Odoo Version         Branch          Status
Odoo 19.0            19.0            ✅ Stable
Odoo 18.0            18.0            ✅ Stable
Odoo 12.0 - 17.0     v.x             ✅ Supported