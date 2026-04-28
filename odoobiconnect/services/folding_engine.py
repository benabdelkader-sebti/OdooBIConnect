from .filter_parser import FilterParser # استيراد الكلاس
from .ast_builder import ASTBuilder # استيراد الكلاس
from .sql_translator import SQLTranslator
from .rls_injector import inject_rls
from .execution_engine import execute_streaming

class FoldingEngine:
    def __init__(self, env):
        self.env = env

    def execute(self, model, params):
        filter_expr = params.get("$filter")
        # ... بقية المتغيرات (select, orderby, top, skip)

        ast = None
        if filter_expr:
            # استخدام الدوال من الكلاسات المصححة
            parsed = FilterParser.parse_filter(filter_expr)
            ast = ASTBuilder.build_ast(parsed)

        # ... (باقي منطق JOIN و Aggregation)

        translator = SQLTranslator(self.env, model)
        sql, sql_params = translator.translate(ast=ast, **params)
        
        sql = inject_rls(self.env, model, sql)
        return execute_streaming(self.env, sql, sql_params)