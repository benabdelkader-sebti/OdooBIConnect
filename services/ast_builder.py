class ASTBuilder:
    def build(self, parsed):
        """دالة اختيارية إذا أردت استخدام الكلاس ككائن"""
        return self.build_ast(parsed)

def build_ast(tokens):
    """
    تقوم هذه الدالة بتحويل قائمة الكلمات المقسمة (Tokens) 
    إلى هيكل بيانات منظم يمكن للمترجم فهمه.
    """
    ast = []
    i = 0
    while i < len(tokens):
        token = tokens[i].strip()
        
        # معالجة الروابط المنطقية والأقواس
        if token.lower() in ["and", "or", "(", ")"]:
            ast.append(token.upper())
            i += 1
        # معالجة التعبيرات (Field Operator Value) مثل: Price gt 100
        elif i + 2 < len(tokens):
            expression = {
                "field": tokens[i],
                "operator": tokens[i+1].lower(),
                "value": tokens[i+2].strip("'")
            }
            ast.append(expression)
            i += 3 # القفز فوق الكلمات الثلاث التي تمت معالجتها
        else:
            # في حال وجود توكن وحيد أو غير مكتمل
            ast.append(token)
            i += 1
            
    return ast