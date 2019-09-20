#!/usr/local/bin/python3

import sys
from error_handler import ErrorHandler
from scanner import Scanner
from parser import Parser
from ast_printer import AstPrinter
from interpreter import Interpreter
from resolver import Resolver

class Lox:
    def __init__(self):
        self.error_handler = ErrorHandler()
        self.interpreter = Interpreter(self.error_handler)

    def run_file(self, path):
        with open(path, "r") as f:
            self.run("".join(f.readlines()))
        if self.error_handler.had_error or self.error_handler.had_runtime_error:
            exit(1)

    def run_prompt(self):
        while True:
            try:
                self.run(input("> "))
                self.error_handler.had_error = False
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
            except EOFError:
                print()
                exit(0)

    def run(self, source):
        scanner = Scanner(self.error_handler, source)
        tokens = scanner.scanTokens()
        parser = Parser(self.error_handler, tokens)
        statements = parser.parse()

        if self.error_handler.had_error:
            return

        resolver = Resolver(self.error_handler, self.interpreter)
        resolver.resolve(statements)

        # Stop if there was a resolution error.
        if self.error_handler.had_error:
            return

        self.interpreter.interpret(statements)

if __name__ == "__main__":
    lox = Lox()
    if len(sys.argv) > 2:
        print("Usage: lox.py [script]")
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()
