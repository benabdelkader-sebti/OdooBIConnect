class QueryContext:

    def __init__(self, env, model_name, user):
        self.env = env
        self.model_name = model_name
        self.user = user
        self.model = env[model_name]
        self.table = self.model._table

    def validate_model(self):
        if self.model_name not in self.env:
            raise Exception("Model not found")

    def get_allowed_fields(self):
        return [
            name for name, field in self.model._fields.items()
            if not field.compute and not field.related
        ]
