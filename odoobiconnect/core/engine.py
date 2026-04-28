from .query_context import QueryContext
from .odata_parser import ODataParser
from .sql_builder import SQLBuilder
from .exceptions import *

class OdooBIEngine:

    def __init__(self, env):
        self.env = env

    def execute(self, model, params):

        context = QueryContext(
            self.env,
            model,
            self.env.user
        )

        context.validate_model()

        parser = ODataParser(params.get("$filter"))
        ast = parser.parse()

        builder = SQLBuilder(context)
        query, values = builder.build_select(ast, params)

        self.env.cr.execute(query, values)

        cols = [c[0] for c in self.env.cr.description]
        rows = self.env.cr.fetchall()

        return {
            "value": [dict(zip(cols, r)) for r in rows]
        }
