from .ast_nodes import ComparisonNode, AndNode, OrNode

class ODataParser:

    def __init__(self, expression):
        self.expression = expression

    def parse(self):

        if not self.expression:
            return None

        if " and " in self.expression:
            left, right = self.expression.split(" and ")
            return AndNode(
                self._parse_simple(left),
                self._parse_simple(right)
            )

        if " or " in self.expression:
            left, right = self.expression.split(" or ")
            return OrNode(
                self._parse_simple(left),
                self._parse_simple(right)
            )

        return self._parse_simple(self.expression)

    def _parse_simple(self, expr):

        for op, symbol in [
            (" eq ", "="),
            (" gt ", ">"),
            (" lt ", "<"),
        ]:
            if op in expr:
                field, value = expr.split(op)
                return ComparisonNode(
                    symbol,
                    field.strip(),
                    value.strip("'")
                )

        raise Exception("Unsupported filter")
