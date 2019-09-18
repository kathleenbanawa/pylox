#!/usr/local/bin/python3

from enum import Enum

class Token:
    def __init__(self, token_type, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal}"

TokenType = Enum("TokenType",
                 "LEFT_PAREN RIGHT_PAREN LEFT_BRACE RIGHT_BRACE \
                  COMMA DOT MINUS PLUS SEMICOLON SLASH STAR \
                  BANG BANG_EQUAL \
                  EQUAL EQUAL_EQUAL \
                  GREATER GREATER_EQUAL \
                  LESS LESS_EQUAL \
                  IDENTIFIER STRING NUMBER \
                  AND CLASS ELSE FALSE FUN FOR IF NIL OR \
                  PRINT RETURN SUPER THIS TRUE VAR WHILE \
                  EOF")
