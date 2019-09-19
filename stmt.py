#!/usr/local/bin/python3

class Stmt:
    def accept(self, visitor):
        return visitor.visit(self)

class BlockStmt(Stmt):
    def __init__(self, statements):
        self.statements = statements

class ExpressionStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression

class PrintStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression

class VariableStmt(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer
