class SQLTranslator:
    def __init__(self, env, model_name):
        self.env = env
        self.model = env[model_name]
        self.table_name = self.model._table

    def translate(self, ast=None, select=None, orderby=None,
                  limit=1000, offset=0,
                  joins=None, groupby=None, aggregates=None):
        
        params = []
        
        # 1. بناء SELECT
        if aggregates:
            select_parts = []
            for agg in aggregates:
                # تأكد من أن func و field مسموح بهما لتجنب Injection
                select_parts.append(f"{agg['func']}({agg['field']}) AS {agg['alias']}")
            if groupby:
                select_parts.extend(groupby)
            fields_clause = ", ".join(select_parts)
        elif select:
            # تنظيف أسماء الحقول
            fields_clause = ", ".join([f"{self.table_name}.{f.strip()}" for f in select.split(",")])
        else:
            fields_clause = f"{self.table_name}.*"

        sql = f"SELECT {fields_clause} FROM {self.table_name}"

        # 2. بناء JOIN
        if joins:
            for join_statement in joins:
                sql += f" {join_statement}"

        # 3. بناء WHERE (منطق مطور)
        if ast:
            where_clauses = []
            # ملاحظة: هذا الجزء يعتمد على شكل الـ AST الذي ينتجه ast_builder.py
            for token in ast:
                if isinstance(token, str) and token.upper() in ["AND", "OR", "(", ")"]:
                    where_clauses.append(token.upper())
                elif isinstance(token, dict): # نفترض أن الـ AST يرسل قاموساً للعمليات
                    field = token.get('field')
                    op = self._map_operator(token.get('operator'))
                    value = token.get('value')
                    
                    where_clauses.append(f"{self.table_name}.{field} {op} %s")
                    params.append(value)
                else:
                    # معالجة النصوص البسيطة كحالة احتياطية (كما في كودك الأصلي مع تحسين)
                    parts = str(token).split(" ")
                    if len(parts) == 3:
                        field, op, val = parts
                        sql_op = self._map_operator(op)
                        where_clauses.append(f"{self.table_name}.{field} {sql_op} %s")
                        params.append(val.strip("'"))

            if where_clauses:
                sql += " WHERE " + " ".join(where_clauses)

        # 4. بناء GROUP BY
        if groupby:
            sql += " GROUP BY " + ", ".join([f"{self.table_name}.{g}" for g in groupby])

        # 5. بناء ORDER BY
        if orderby:
            # حماية بسيطة للـ Order By
            safe_order = "".join(c for c in orderby if c.isalnum() or c in " ,_")
            sql += f" ORDER BY {safe_order}"

        # 6. LIMIT & OFFSET
        if not aggregates:
            sql += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

        return sql, params

    def _map_operator(self, odata_op):
        mapping = {
            'eq': '=', 'ne': '!=', 'gt': '>', 'ge': '>=',
            'lt': '<', 'le': '<=', 'contains': 'LIKE'
        }
        return mapping.get(odata_op.lower(), '=')