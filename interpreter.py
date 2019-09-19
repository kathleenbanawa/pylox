#!/usr/local/bin/python3

from token import TokenType as TT
from visitor import Visitor
from expr import *
from stmt import *
from environment import Environment
from error_handler import LoxRuntimeException

class Interpreter(Visitor):
    def __init__(self, error_handler):
        self.error_handler = error_handler
        self.environment = Environment()

    def visit(self, x):
        if isinstance(x, AssignExpr):
            value = self.evaluate(x.value)
            self.environment.assign(x.name, value)
            return value
        elif isinstance(x, BinaryExpr):
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
        elif isinstance(x, VariableExpr):
            return self.environment.get(x.name)
        elif isinstance(x, LiteralExpr):
            return x.value
        elif isinstance(x, GroupingExpr):
            return self.evaluate(x.expression)
        elif isinstance(x, ExpressionStmt):
            self.evaluate(x.expression)
            return None
        elif isinstance(x, BlockStmt):
            self.executeBlock(x.statements, Environment(self.environment))
            return None
        elif isinstance(x, PrintStmt):
            value = self.evaluate(x.expression)
            print(self.stringify(value))
            return None
        elif isinstance(x, VariableStmt):
            value = None
            if x.initializer:
                value = self.evaluate(x.initializer)
            self.environment.define(x.name.lexeme, value)
            return None

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
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

    def execute(self, stmt):
        return stmt.accept(self)

    def executeBlock(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
