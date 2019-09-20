#!/usr/local/bin/python3

from token import Token
from lox_types import TokenType as TT

class ErrorHandler:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def error(self, x, message):
        if isinstance(x, Token):
            if x.token_type == TT.EOF:
                self.report(x.line, " at end", message)
            else:
                self.report(x.line, f" at '{x.lexeme}'", message)
        else:
            self.report(line, "", message)

    def runtimeError(self, error):
        print(error)
        self.had_runtime_error = True

    def report(self, line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        self.had_error = True

class LoxParseException(Exception):
    pass

class LoxRuntimeException(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message
    def __str__(self):
        return f"{self.message}\n[line {self.token.line}]"
