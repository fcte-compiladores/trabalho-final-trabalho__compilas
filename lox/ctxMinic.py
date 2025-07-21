class Ctx:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {} if parent is None else parent.functions
        self.classes = {} if parent is None else parent.classes
        self.parent = parent
        self.expected_return_type = None

    def get(self, name):
        if name in self.variables:
            return self.variables[name]["value"]
        elif self.parent:
            return self.parent.get(name)
        elif name in self.functions:
            return self.functions[name]
        elif name in self.classes:
            return self.classes[name]
        else:
            raise NameError(f"'{name}' não encontrado no contexto.")

    def get_type(self, name):
        if name in self.variables:
            return self.variables[name]["type"]
        elif self.parent:
            return self.parent.get_type(name)
        else:
            raise NameError(f"Tipo da variável '{name}' não encontrado no contexto.")

    def var_def(self, name, tipo, value):
        self.variables[name] = {"type": tipo, "value": value}

    def set_var(self, name, value):
        if name in self.variables:
            tipo = self.variables[name]["type"]
            if not check_type(tipo, value):
                raise TypeError(f"Tipo incorreto na atribuição para '{name}': esperado {tipo}, recebeu {type(value).__name__}")
            self.variables[name]["value"] = value
        elif self.parent:
            self.parent.set_var(name, value)
        else:
            raise NameError(f"Variável '{name}' não declarada.")

    def set_function(self, name, func):
        self.functions[name] = func

    def set_class(self, name, cls):
        self.classes[name] = cls

    def copy(self):
        new_ctx = Ctx(parent=self)
        new_ctx.expected_return_type = self.expected_return_type
        return new_ctx

def check_type(tipo: str, val) -> bool:
    if tipo == "int":
        return isinstance(val, int)
    elif tipo == "char":
        return isinstance(val, str) and len(val) == 1
    elif tipo == "bool":
        return isinstance(val, bool)
    return False
