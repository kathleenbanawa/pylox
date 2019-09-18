#!/usr/local/bin/python3

class ErrorHandler:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def error(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        self.had_error = True

