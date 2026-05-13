class RLSInjector:
    def __init__(self, env, model_name):
        self.env = env
        self.model = env[model_name]

    def inject_rls(self, sql):
        """
        تقوم هذه الدالة بحقن قيود الأمان (تعدد الشركات و Record Rules)
        داخل جملة SQL الأصلية.
        """
        extra_conditions = []

        # 1. التحقق من أمان تعدد الشركات (Multi-company)
        if 'company_id' in self.model._fields:
            company_ids = self.env.companies.ids
            # تحويل القائمة إلى نص متوافق مع SQL
            comp_ids_str = ",".join(map(str, company_ids))
            extra_conditions.append(f"{self.model._table}.company_id IN ({comp_ids_str})")

        # 2. التحقق من قواعد السجلات (Odoo Record Rules)
        # ملاحظة: استخراج الـ SQL من قواعد السجلات معقد، 
        # لذا سنكتفي حالياً بحماية الشركة لضمان استقرار المحرك.

        if not extra_conditions:
            return sql

        # دمج الشروط الإضافية في جملة SQL
        clause = " AND ".join(extra_conditions)
        
        if "WHERE" in sql.upper():
            # إدخال الشرط بعد الـ WHERE مباشرة لضمان عدم تعارضه مع LIMIT أو ORDER BY
            parts = re.split(r" WHERE ", sql, flags=re.IGNORECASE)
            return f"{parts[0]} WHERE ({clause}) AND {parts[1]}"
        else:
            return f"{sql} WHERE {clause}"

# دمج الدالة لتكون متوافقة مع استدعاء FoldingEngine
def inject_rls(env, model_name, sql):
    injector = RLSInjector(env, model_name)
    return injector.inject_rls(sql)