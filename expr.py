#!/usr/local/bin/python3

class Expr:
    def accept(self, visitor):
        return visitor.visit(self)

class AssignExpr(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        return f"{self.name} {self.value}"

class BinaryExpr(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def __str__(self):
        return f"{self.left} {self.operator} {self.right}"

class UnaryExpr(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
    def __str__(self):
        return f"{self.operator} {self.right}"

class LiteralExpr(Expr):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"{self.value}"

class GroupingExpr(Expr):
    def __init__(self, expression):
        self.expression = expression
    def __str__(self):
        return f"{self.expression}"

class VariableExpr(Expr):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"{name}"
