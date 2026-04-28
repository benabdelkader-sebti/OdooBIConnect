class QueryOptimizer:

    def validate(self, sql):
        forbidden = ["insert", "update", "delete", "drop"]
        for word in forbidden:
            if word in sql.lower():
                raise Exception("Forbidden query")
