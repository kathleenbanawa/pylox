#!/usr/local/bin/python3

from visitor import Visitor
from expr import *

class AstPrinter(Visitor):
    def visit(self, x):
        if isinstance(x, BinaryExpr):
            return self.parenthesize(x.operator.lexeme, x.left, x.right)
        elif isinstance(x, UnaryExpr):
            return self.parenthesize(x.operator.lexeme, x.right)
        elif isinstance(x, LiteralExpr):
            return x.value
        elif isinstance(x, GroupingExpr):
            return self.parenthesize("group", x.expression)

    def print_ast(self, expr):
        return expr.accept(self)

    def parenthesize(self, name, *args):
        rt = f"({name}"
        for arg in args:
            if arg:
                rt += f" {arg.accept(self)}"
        rt += f")"
        return rt
