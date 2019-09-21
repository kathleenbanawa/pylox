#!/usr/local/bin/python3

class Stmt:
    def accept(self, visitor):
        return visitor.visit(self)

class BlockStmt(Stmt):
    def __init__(self, statements):
        self.statements = statements

class ClassStmt(Stmt):
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

class ExpressionStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression

class IfStmt(Stmt):
    def __init__(self, condition, thenBranch, elseBranch):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

class FunctionStmt(Stmt):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class PrintStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression

class ReturnStmt(Stmt):
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value

class VariableStmt(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

class WhileStmt(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
