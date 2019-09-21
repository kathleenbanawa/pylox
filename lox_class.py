from lox_callable import LoxCallable
from lox_instance import LoxInstance

class LoxClass(LoxCallable):
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def findMethod(self, name):
        if name in self.methods:
            return self.methods[name]
        if self.superclass:
            return self.superclass.findMethod(name)
        return None

    def call(self, interpreter, arguments):
        instance = LoxInstance(self)
        initializer = self.findMethod("init")
        if initializer:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def arity(self):
        initializer = self.findMethod("init")
        if not initializer:
            return 0
        return initializer.arity()

    def __str__(self):
        return self.name
