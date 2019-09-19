#!/usr/local/bin/python3

from token import TokenType as TT
from expr import *
from stmt import *
from error_handler import LoxParseException

class Parser:
    def __init__(self, error_handler, tokens):
        self.error_handler = error_handler

        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements

    def expression(self):
        return self.assignment()

    def declaration(self):
        try:
            if self.match(TT.VAR):
                return self.varDeclaration()
            return self.statement()
        except LoxParseException:
            self.synchronize()
            return None

    def statement(self):
        if self.match(TT.PRINT):
            return self.printStatement()
        if self.match(TT.LEFT_BRACE):
            return BlockStmt(self.block())
        return self.expressionStatement()

    def printStatement(self):
        value = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)

    def varDeclaration(self):
        name = self.consume(TT.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TT.EQUAL):
            initializer = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after variable declaration.")
        return VariableStmt(name, initializer)

    def expressionStatement(self):
        expr = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after value.")
        return ExpressionStmt(expr)

    def block(self):
        statements = []
        while not self.check(TT.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())
        self.consume(TT.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def assignment(self):
        expr = self.equality()
        if self.match(TT.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, VariableExpr):
                name = expr.name
                return AssignExpr(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TT.BANG_EQUAL, TT.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.addition()
        while self.match(TT.GREATER, TT.GREATER_EQUAL, TT.LESS, TT.LESS_EQUAL):
            operator = self.previous()
            right = self.addition()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def addition(self):
        expr = self.multiplication()
        while self.match(TT.MINUS, TT.PLUS):
            operator = self.previous()
            right = self.multiplication()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def multiplication(self):
        expr = self.unary()
        while self.match(TT.SLASH, TT.STAR):
            operator = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TT.BANG, TT.MINUS):
            operator = self.previous()
            right = self.unary()
            return UnaryExpr(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TT.FALSE):
            return LiteralExpr(False)
        if self.match(TT.TRUE):
            return LiteralExpr(True)
        if self.match(TT.NIL):
            return LiteralExpr(None)

        if self.match(TT.NUMBER, TT.STRING):
            return LiteralExpr(self.previous().literal)

        if self.match(TT.IDENTIFIER):
            return VariableExpr(self.previous())

        if self.match(TT.LEFT_PAREN):
            expr = self.expression()
            self.consume(TT.RIGHT_PAREN, "Except ')' after expression.")
            return GroupingExpr(expr)

    def match(self, *token_types):
        for t in token_types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        self.error(self.peek(), message)

    def check(self, token_type):
        if self.isAtEnd():
            return False
        return self.peek().token_type == token_type

    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def isAtEnd(self):
        return self.peek().token_type == TT.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current-1]

    def error(self, token, message):
        self.error_handler.error(token, message)
        raise(LoxParseException())

    def synchronize(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().token_type == TT.SEMICOLON:
                return
            tt = self.peek().token_type
            if tt in [TT.CLASS, TT.FUN, TT.VAR, TT.FOR, TT.IF, TT.WHILE, TT.PRINT, TT.RETURN]:
                return
        self.advance()
