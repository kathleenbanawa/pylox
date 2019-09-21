from error_handler import LoxRuntimeException

class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.klass.findMethod(name.lexeme)
        if method:
            return method.bind(self)

        raise(LoxRuntimeException(name, f"Undefined property '{name.lexeme}'"))

    def set(self, name, value):
        self.fields[name.lexeme] = value

    def __str__(self):
        return f"{self.klass.name} instance"
