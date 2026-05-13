class JoinResolver:

    def __init__(self, env, model):
        self.env = env
        self.model = model
        self.base_table = env[model]._table

    def resolve_expand(self, expand):
        """
        expand example:
        country_id($select=name)
        """
        joins = []
        select_fields = []

        if not expand:
            return joins, select_fields

        model_obj = self.env[self.model]

        parts = expand.split("(")
        relation_field = parts[0]

        field = model_obj._fields.get(relation_field)
        if not field:
            return joins, select_fields

        target_model = field.comodel_name
        target_table = self.env[target_model]._table

        join_clause = f"""
        LEFT JOIN {target_table} AS {relation_field}
        ON {self.base_table}.{relation_field} = {relation_field}.id
        """

        joins.append(join_clause)

        if "$select=" in expand:
            selected = expand.split("$select=")[1].replace(")", "")
            for f in selected.split(","):
                select_fields.append(f"{relation_field}.{f.strip()} AS {relation_field}_{f.strip()}")

        return joins, select_fields
