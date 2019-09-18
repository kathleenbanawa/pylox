#!/usr/local/bin/python3

from token import Token, TokenType as TT

class Scanner:
    def __init__(self, error_handler, source):
        self.error_handler = error_handler

        self.source = source
        self.tokens = []

        self.start = 0
        self.current = 0
        self.line = 1

        self.keywords = {
            "and": TT.AND,
            "class": TT.CLASS,
            "else": TT.ELSE,
            "false": TT.FALSE,
            "for": TT.FOR,
            "fun": TT.FUN,
            "if": TT.IF,
            "nil": TT.NIL,
            "or": TT.OR,
            "print": TT.PRINT,
            "return": TT.RETURN,
            "super": TT.SUPER,
            "this": TT.THIS,
            "true": TT.TRUE,
            "var": TT.VAR,
            "while": TT.WHILE
        }

    def scanTokens(self):
        while not self.isAtEnd():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TT.EOF, "", None, self.line))
        return self.tokens

    def scanToken(self):
        c = self.advance()
        if c == '(':
            self.addToken(TT.LEFT_PAREN)
        elif c == ')':
            self.addToken(TT.RIGHT_PAREN)
        elif c == '{':
            self.addToken(TT.LEFT_BRACE)
        elif c == '}':
            self.addToken(TT.RIGHT_BRACE)
        elif c == ',':
            self.addToken(TT.COMMA)
        elif c == '.':
            self.addToken(TT.DOT)
        elif c == '-':
            self.addToken(TT.MINUS)
        elif c == '+':
            self.addToken(TT.PLUS)
        elif c == ';':
            self.addToken(TT.SEMICOLON)
        elif c == '*':
            self.addToken(TT.STAR)
        elif c == '!':
            self.addToken(TT.BANG_EQUAL if self.match('=') else TT.BANG)
        elif c == '=':
            self.addToken(TT.EQUAL_EQUAL if self.match('=') else TT.EQUAL)
        elif c == '<':
            self.addToken(TT.LESS_EQUAL if self.match('=') else TT.LESS)
        elif c == '>':
            self.addToken(TT.GREATER_EQUAL if self.match('=') else TT.GREATER)
        elif c == '/':
            if self.match('/'):
                # A comment goes until the end of the line.
                while self.peek() != '\n' and not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(TT.SLASH)
        elif c in [' ', '\r', '\t']:
            # Ignore whitespace.
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if self.isDigit(c):
                self.number()
            elif self.isAlpha(c):
                self.identifier()
            else:
                self.error_handler.error(self.line, "Unexpected character.")

    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        token_type = None
        if text in self.keywords:
            token_type = self.keywords[text]
        if not token_type:
            token_type = TT.IDENTIFIER
        self.addToken(token_type)

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()

        # Look for a fractional part.
        if self.peek() == '.' and self.isDigit(self.peekNext()):
            # Consume the "."
            self.advance()

            while self.isDigit(self.peek()):
                self.advance()

        self.addToken(TT.NUMBER, float(self.source[self.start:self.current]))

    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        # Unterminated string.
        if self.isAtEnd():
            self.error_handler.error(self.line, "Unterminated string.")
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start+1:self.current-1]
        self.addToken(TT.STRING, value)

    def match(self, expected):
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    def peekNext(self):
        if self.current+1 >= len(self.source):
            return '\0'
        return self.source[self.current+1]

    def isAlpha(self, c):
        return c.isalpha() or c == '_'

    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)

    def isDigit(self, c):
        return c.isdigit()

    def isAtEnd(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current-1]

    def addToken(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
