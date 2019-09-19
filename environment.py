#!/usr/local/bin/python3

from error_handler import LoxRuntimeException

class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        raise(LoxRuntimeException(name, f"Undefined variable '{name.lexeme}'."))

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        raise(LoxRuntimeException(name, f"Undefined variable '{name.lexeme}'."))
