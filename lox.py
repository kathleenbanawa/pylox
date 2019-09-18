#!/usr/local/bin/python3

import sys
from error_handler import ErrorHandler
from scanner import Scanner

class Lox:
    def __init__(self):
        self.error_handler = ErrorHandler()

    def run_file(self, path):
        with open(path, "r") as f:
            self.run("".join(f.readlines()))
        if self.error_handler.had_error or self.error_handler.had_runtime_error:
            exit(1)

    def run_prompt(self):
        while True:
            self.run(input("> "))
            self.error_handler.had_error = False

    def run(self, source):
        scanner = Scanner(self.error_handler, source)
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token)

if __name__ == "__main__":
    lox = Lox()
    if len(sys.argv) > 2:
        print("Usage: lox.py [script]")
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()
