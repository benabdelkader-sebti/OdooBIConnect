class QueryGovernor:

    def __init__(self, cr, max_cost=50000):
        self.cr = cr
        self.max_cost = max_cost

    def validate(self, query, params):

        explain_query = "EXPLAIN (FORMAT JSON) " + query.as_string(self.cr)
        self.cr.execute(explain_query, params)
        result = self.cr.fetchone()[0][0]

        cost = result["Plan"]["Total Cost"]

        if cost > self.max_cost:
            raise Exception("Query too expensive")
