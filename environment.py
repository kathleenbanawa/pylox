#!/usr/local/bin/python3

from error_handler import LoxRuntimeException

class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def ancestor(self, distance):
        environment = self
        for i in range(0, distance):
            environment = environment.enclosing
        return environment

    def getAt(self, distance, name):
        return self.ancestor(distance).values[name]

    def assignAt(self, distance, name, value):
        self.ancestor(distance).values[name.lexeme] = value

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
