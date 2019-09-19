#!/usr/local/bin/python3

class ErrorHandler:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def error(self, line, message):
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
