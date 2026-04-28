import re

class FilterParser:
    def __init__(self, expression):
        self.expression = expression

    def parse(self):
        if not self.expression:
            return None
        if " eq " in self.expression:
            field, val = self.expression.split(" eq ")
            return ("eq", field.strip(), val.strip("'"))
        return None

    @staticmethod
    def parse_filter(filter_string):
        """تقسيم نص الفلتر إلى قطع منطقية"""
        tokens = re.split(r"\s+(and|or)\s+", filter_string)
        return tokens