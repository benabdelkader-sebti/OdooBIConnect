# -*- coding: utf-8 -*-
from lxml import etree

class MetadataService:
    def __init__(self, env):
        self.env = env

    def generate_metadata(self, models_to_export):
        """توليد ملف XML بصيغة OData Conceptual Schema (CSDL)"""
        root = etree.Element("edmx:Edmx", Version="4.0", xmlns_edmx="http://docs.oasis-open.org/odata/ns/edmx")
        data_services = etree.SubElement(root, "edmx:DataServices")
        schema = etree.SubElement(data_services, "Schema", Namespace="OdooNamespace", xmlns="http://docs.oasis-open.org/odata/ns/edm")

        for model_name in models_to_export:
            model = self.env['ir.model'].search([('model', '=', model_name)], limit=1)
            if not model: continue

            entity_type = etree.SubElement(schema, "EntityType", Name=model_name.replace('.', '_'))
            etree.SubElement(entity_type, "Key").append(etree.Element("PropertyRef", Name="id"))
            etree.SubElement(entity_type, "Property", Name="id", Type="Edm.Int32", Nullable="false")

            # استخراج الحقول والعلاقات
            fields = self.env[model_name].fields_get()
            for field_name, field_data in fields.items():
                if field_data['type'] in ['char', 'text']:
                    etree.SubElement(entity_type, "Property", Name=field_name, Type="Edm.String")
                elif field_data['type'] == 'many2one':
                    # تعريف علاقة الربط ليراها Power BI
                    etree.SubElement(entity_type, "NavigationProperty", 
                                    Name=field_name, 
                                    Type=f"OdooNamespace.{field_data['relation'].replace('.', '_')}")

        return etree.tostring(root, xml_declaration=True, encoding='utf-8')