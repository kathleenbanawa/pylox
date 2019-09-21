#!/usr/local/bin/python3

from lox_types import TokenType as TT
from visitor import Visitor
from expr import *
from stmt import *
from environment import Environment
from lox_function import LoxFunction
from lox_callable import LoxCallable
from lox_return import LoxReturn
from lox_class import LoxClass
from lox_instance import LoxInstance
from error_handler import LoxRuntimeException

class Interpreter(Visitor):
    def __init__(self, error_handler):
        self.error_handler = error_handler
        self.globals = Environment()
        self.environment = self.globals
        self.locals = {}

    def visit(self, x):
        if isinstance(x, AssignExpr):
            value = self.evaluate(x.value)

            if x in self.locals:
                distance = self.locals[x]
                if distance is not None:
                    self.environment.assignAt(distance, x.name, value)
            else:
                self.globals.assign(x.name, value)

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
        elif isinstance(x, CallExpr):
            callee = self.evaluate(x.callee)
            arguments = []
            for argument in x.arguments:
                arguments.append(self.evaluate(argument))
            if not isinstance(callee, LoxCallable):
                raise(LoxRuntimeException(x.paren, "Can only call functions and classes."))
            function = callee
            if len(arguments) != function.arity():
                raise(LoxRuntimeException(x.paren, f"Expected {function.arity()} arguments but got {len(arguments)}."))
            return function.call(self, arguments)
        elif isinstance(x, GetExpr):
            obj = self.evaluate(x.obj)
            if isinstance(obj, LoxInstance):
                return obj.get(x.name)
            raise(LoxRuntimeException(x.name, "Only instances have properties."))
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
            return self.lookUpVariable(x.name, x)
        elif isinstance(x, LiteralExpr):
            return x.value
        elif isinstance(x, LogicalExpr):
            left = self.evaluate(x.left)
            if x.operator.type == TT.OR:
                if self.isTruthy(left):
                    return left
            else:
                if not self.isTruthy(left):
                    return left
            return self.evaluate(x.right)
        elif isinstance(x, SetExpr):
            obj = self.evaluate(x.obj)
            if not isinstance(obj, LoxInstance):
                raise(LoxRuntimeException(x.name, "Only instances have fields."))
            value = self.evaluate(x.value)
            obj.set(x.name, value)
            return value
        elif isinstance(x, ThisExpr):
            return self.lookUpVariable(x.keyword, x)
        elif isinstance(x, GroupingExpr):
            return self.evaluate(x.expression)
        elif isinstance(x, ExpressionStmt):
            self.evaluate(x.expression)
            return None
        elif isinstance(x, BlockStmt):
            self.executeBlock(x.statements, Environment(self.environment))
            return None
        elif isinstance(x, ClassStmt):
            self.environment.define(x.name.lexeme, None)

            methods = {}
            for method in x.methods:
                function = LoxFunction(method, self.environment, method.name.lexeme == "init")
                methods[method.name.lexeme] = function

            klass = LoxClass(x.name.lexeme, methods)
            self.environment.assign(x.name, klass)
            return None
        elif isinstance(x, FunctionStmt):
            function = LoxFunction(x, self.environment)
            self.environment.define(x.name.lexeme, function)
            return None
        elif isinstance(x, IfStmt):
            if self.isTruthy(self.evaluate(x.condition)):
                self.execute(x.thenBranch)
            elif x.elseBranch:
                self.execute(x.elseBranch)
            return None
        elif isinstance(x, PrintStmt):
            value = self.evaluate(x.expression)
            print(self.stringify(value))
            return None
        elif isinstance(x, ReturnStmt):
            value = None
            if x.value:
                value = self.evaluate(x.value)
            raise(LoxReturn(value))
        elif isinstance(x, VariableStmt):
            value = None
            if x.initializer:
                value = self.evaluate(x.initializer)
            self.environment.define(x.name.lexeme, value)
            return None
        elif isinstance(x, WhileStmt):
            while self.isTruthy(self.evaluate(x.condition)):
                self.execute(x.body)
            return None

    def lookUpVariable(self, name, expr):
        if expr in self.locals:
            distance = self.locals[expr]
            if distance is not None:
                return self.environment.getAt(distance, name.lexeme)
        else:
            return self.globals.get(name)

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

    def resolve(self, expr, depth):
        self.locals[expr] = depth

    def executeBlock(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
