from psycopg2 import sql

class SQLBuilder:

    def __init__(self, context):
        self.context = context

    def build_select(self, ast, params):

        table = sql.Identifier(self.context.table)

        query = sql.SQL("SELECT * FROM {}").format(table)

        values = []

        if ast:
            query += sql.SQL(" WHERE ") + self._build_where(ast, values)

        limit = int(params.get("$top", 1000))
        offset = int(params.get("$skip", 0))

        query += sql.SQL(" LIMIT %s OFFSET %s")
        values.extend([limit, offset])

        return query, values

    def _build_where(self, node, values):

        if node.operator == "=":
            values.append(node.value)
            return sql.SQL("{} = %s").format(
                sql.Identifier(node.field)
            )
