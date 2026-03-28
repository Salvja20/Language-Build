INTEGER    = 'INTEGER'
IDENTIFIER = 'IDENTIFIER'
PLUS       = 'PLUS'
MINUS      = 'MINUS'
STAR       = 'STAR'
SLASH      = 'SLASH'
EQUAL      = 'EQUAL'
SEMICOLON  = 'SEMICOLON'
LPAREN     = 'LPAREN'
RPAREN     = 'RPAREN'
PRINT      = 'PRINT'
EOF        = 'EOF'

KEYWORDS = {'print': PRINT}


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0

    def error(self, char):
        raise LexerError(f"Unknown character: '{char}'")

    def peek(self):
        if self.pos < len(self.source):
            return self.source[self.pos]
        return None

    def advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        return ch

    def skip_whitespace(self):
        while self.peek() is not None and self.peek().isspace():
            self.advance()

    def read_integer(self):
        digits = ''
        while self.peek() is not None and self.peek().isdigit():
            digits += self.advance()
        return Token(INTEGER, int(digits))

    def read_identifier(self):
        chars = ''
        while self.peek() is not None and (self.peek().isalnum() or self.peek() == '_'):
            chars += self.advance()
        token_type = KEYWORDS.get(chars, IDENTIFIER)
        return Token(token_type, chars)

    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            self.skip_whitespace()
            if self.pos >= len(self.source):
                break

            ch = self.peek()

            if ch.isdigit():
                tokens.append(self.read_integer())
            elif ch.isalpha() or ch == '_':
                tokens.append(self.read_identifier())
            elif ch == '+':
                self.advance()
                tokens.append(Token(PLUS, '+'))
            elif ch == '-':
                self.advance()
                tokens.append(Token(MINUS, '-'))
            elif ch == '*':
                self.advance()
                tokens.append(Token(STAR, '*'))
            elif ch == '/':
                self.advance()
                tokens.append(Token(SLASH, '/'))
            elif ch == '=':
                self.advance()
                tokens.append(Token(EQUAL, '='))
            elif ch == ';':
                self.advance()
                tokens.append(Token(SEMICOLON, ';'))
            elif ch == '(':
                self.advance()
                tokens.append(Token(LPAREN, '('))
            elif ch == ')':
                self.advance()
                tokens.append(Token(RPAREN, ')'))
            else:
                self.error(ch)

        tokens.append(Token(EOF, 'EOF'))
        return tokens
