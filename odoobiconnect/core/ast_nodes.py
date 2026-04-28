class ASTNode:
    pass


class ComparisonNode(ASTNode):
    def __init__(self, operator, field, value):
        self.operator = operator
        self.field = field
        self.value = value


class AndNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class OrNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
