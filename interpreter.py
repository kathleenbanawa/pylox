#!/usr/local/bin/python3

from token import TokenType as TT
from visitor import Visitor
from expr import *
from error_handler import LoxRuntimeException

class Interpreter(Visitor):
    def __init__(self, error_handler):
        self.error_handler = error_handler

    def visit(self, x):
        if isinstance(x, BinaryExpr):
            left = self.evaluate(x.left)
            right = self.evaluate(x.right)

            tt = x.operator.token_type
            if tt == TT.GREATER:
                self.checkNumberOperands(x.operator, left, right)
                return left > right
            elif tt == TT.GREATER_EQUAL:
                self.checkNumberOperands(x.operator, left, right)
                return left >= right
            elif tt == TT.LESS:
                self.checkNumberOperands(x.operator, left, right)
                return left < right
            elif tt == TT.LESS_EQUAL:
                self.checkNumberOperands(x.operator, left, right)
                return left <= right
            elif tt == TT.MINUS:
                self.checkNumberOperands(x.operator, left, right)
                return left - right
            elif tt == TT.PLUS:
                if type(left) == type(right):
                    return left + right
                raise(LoxRuntimeException(x.operator, "Operands must be two numbers or two strings."))
            elif tt == TT.SLASH:
                self.checkNumberOperands(x.operator, left, right)
                return left // right
            elif tt == TT.STAR:
                self.checkNumberOperands(x.operator, left, right)
                return left * right
            elif tt == TT.BANG_EQUAL:
                return not self.isEqual(left, right)
            elif tt == TT.EQUAL_EQUAL:
                return self.isEqual(left, right)

            # Unreachable.
            return None
        elif isinstance(x, UnaryExpr):
            right = self.evaluate(x.right)

            tt = x.operator.token_type
            if tt == TT.BANG:
                return not self.isTruthy(right)
            elif tt == TT.MINUS:
                self.checkNumberOperand(x.operator, right)
                return -right

            # Unreachable.
            return None
        elif isinstance(x, LiteralExpr):
            return x.value
        elif isinstance(x, GroupingExpr):
            return self.evaluate(x.expression)

    def interpret(self, expression):
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except LoxRuntimeException as e:
            self.error_handler.runtimeError(e)

    def checkNumberOperand(self, operator, operand):
        if isinstance(operand, int) or isinstance(operand, float):
            return
        raise(LoxRuntimeException(operator, "Operand must be a number."))

    def checkNumberOperands(self, operator, left, right):
        if isinstance(left, int) and isinstance(right, int):
            return
        if isinstance(left, float) and isinstance(right, float):
            return
        raise(LoxRuntimeException(operator, "Operands must be numbers."))

    def isTruthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def isEqual(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def stringify(self, obj):
        if obj is None:
            return "nil"
        return obj

    def evaluate(self, expr):
        return expr.accept(self)
