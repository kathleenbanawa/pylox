#!/usr/local/bin/python3

from visitor import Visitor
from stmt import *
from expr import *
from lox_types import FunctionType as FT, ClassType as CT

class Resolver(Visitor):
    def __init__(self, error_handler, interpreter):
        self.error_handler = error_handler
        self.interpreter = interpreter
        self.scopes = []
        self.currentFunction = FT.NONE
        self.currentClass = CT.NONE

    def resolve(self, x):
        if isinstance(x, list):
            for statement in x:
                self.resolve(statement)
        else:
            x.accept(self)

    def resolveFunction(self, function, function_type):
        enclosingFunction = self.currentFunction
        self.currentFunction = function_type

        self.beginScope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.endScope()

        self.currentFunction = enclosingFunction

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop()

    def declare(self, name):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.error_handler.error(name, "Variable with this name already declared in this scope.")
        scope[name.lexeme] = False

    def define(self, name):
        if len(self.scopes) == 0:
            return
        self.scopes[-1][name.lexeme] = True

    def resolveLocal(self, expr, name):
        for i in range(len(self.scopes)-1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes)-1-i)
                return
        # Not found. Assume it is global.

    def visit(self, x):
        if isinstance(x, BlockStmt):
            self.beginScope()
            self.resolve(x.statements)
            self.endScope()
        elif isinstance(x, ClassStmt):
            enclosingClass = self.currentClass
            self.currentClass = CT.CLASS

            self.declare(x.name)
            self.define(x.name)

            self.beginScope()
            self.scopes[-1]["this"] = True

            for method in x.methods:
                declaration = FT.METHOD
                if method.name.lexeme == "init":
                    declaration = FT.INITIALIZER
                self.resolveFunction(method, declaration)

            self.endScope()
            self.currenttClass = enclosingClass
        elif isinstance(x, ExpressionStmt):
            self.resolve(x.expression)
        elif isinstance(x, FunctionStmt):
            self.declare(x.name)
            self.define(x.name)
            self.resolveFunction(x, FT.FUNCTION)
        elif isinstance(x, IfStmt):
            self.resolve(x.condition)
            self.resolve(x.thenBranch)
            if x.elseBranch:
                self.resolve(x.elseBranch)
        elif isinstance(x, PrintStmt):
            self.resolve(x.expression)
        elif isinstance(x, ReturnStmt):
            if self.currentFunction == FT.NONE:
                self.error_handler.error(x.keyword, "Cannot return from top-level code.")
            if x.value:
                if self.currentFunction == FT.INITIALIZER:
                    self.error_handler.error(x.keyword, "Cannot return a value from an initializer.")
                self.resolve(x.value)
        elif isinstance(x, VariableStmt):
            self.declare(x.name)
            if x.initializer:
                self.resolve(x.initializer)
            self.define(x.name)
        elif isinstance(x, WhileStmt):
            self.resolve(x.conition)
            self.resolve(x.body)
        elif isinstance(x, AssignExpr):
            self.resolve(x.value)
            self.resolveLocal(x, x.name)
        elif isinstance(x, BinaryExpr):
            self.resolve(x.left)
            self.resolve(x.right)
        elif isinstance(x, CallExpr):
            self.resolve(x.callee)
            for argument in x.arguments:
                self.resolve(argument)
        elif isinstance(x, GetExpr):
            self.resolve(x.obj)
        elif isinstance(x, GroupingExpr):
            self.resolve(x.expression)
        elif isinstance(x, LiteralExpr):
            pass
        elif isinstance(x, LogicalExpr):
            self.resolve(x.left)
            self.resolve(x.right)
        elif isinstance(x, SetExpr):
            self.resolve(x.value)
            self.resolve(x.obj)
        elif isinstance(x, ThisExpr):
            if self.currentClass == CT.NONE:
                self.error_handler.error(x.keyword, "Cannot use 'this' outside of a class.")
                return None
            self.resolveLocal(x, x.keyword)
        elif isinstance(x, UnaryExpr):
            self.resolve(right)
        elif isinstance(x, VariableExpr):
            if len(self.scopes) > 0 and x.name.lexeme in self.scopes[-1]:
                if self.scopes[-1][x.name.lexeme] == False:
                    self.error_handler.error(x.name, "Cannot read local variable in its own initializer.")
            self.resolveLocal(x, x.name)
        return None
