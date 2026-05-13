class AggregationEngine:

    def __init__(self):
        pass

    def parse_apply(self, apply_expr):
        """
        Example:
        groupby((country_id), aggregate(amount_total with sum as Total))
        """

        if not apply_expr:
            return None

        result = {
            "groupby": [],
            "aggregates": []
        }

        if "groupby" in apply_expr:
            group_part = apply_expr.split("groupby((")[1].split("))")[0]
            result["groupby"] = [f.strip() for f in group_part.split(",")]

        if "aggregate" in apply_expr:
            agg_part = apply_expr.split("aggregate(")[1].split(")")[0]
            parts = agg_part.split(" with ")
            field = parts[0].strip()
            func_alias = parts[1].split(" as ")
            func = func_alias[0].strip()
            alias = func_alias[1].strip()

            result["aggregates"].append({
                "field": field,
                "func": func.upper(),
                "alias": alias
            })

        return result
