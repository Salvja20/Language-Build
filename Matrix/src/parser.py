from lexer import (
    Token, INTEGER, IDENTIFIER, PLUS, MINUS,
    STAR, SLASH, EQUAL, SEMICOLON, LPAREN, RPAREN, PRINT, EOF
)
from ast_nodes import (
    Program, AssignmentStatement, PrintStatement,
    BinaryExpression, IntegerLiteral, Identifier
)


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def expect(self, token_type):
        token = self.current()
        if token.type != token_type:
            raise ParseError(
                f"Expected {token_type} but got {token.type}('{token.value}')"
            )
        return self.advance()

    
    def parse_program(self):
        statements = []
        while self.current().type != EOF:
            statements.append(self.parse_statement())
        return Program(statements)

    
    def parse_statement(self):
        if self.current().type == PRINT:
            return self.parse_print()
        elif self.current().type == IDENTIFIER:
            return self.parse_assignment()
        else:
            tok = self.current()
            raise ParseError(f"Unexpected token {tok.type}('{tok.value}')")

    
    def parse_assignment(self):
        name = self.expect(IDENTIFIER).value
        self.expect(EQUAL)
        expr = self.parse_expression()
        self.expect(SEMICOLON)
        return AssignmentStatement(Identifier(name), expr)

   
    def parse_print(self):
        self.expect(PRINT)
        expr = self.parse_expression()
        self.expect(SEMICOLON)
        return PrintStatement(expr)

    
    def parse_expression(self):
        left = self.parse_term()
        while self.current().type in (PLUS, MINUS):
            op = self.advance().value
            right = self.parse_term()
            left = BinaryExpression(left, op, right)
        return left

    
    def parse_term(self):
        left = self.parse_factor()
        while self.current().type in (STAR, SLASH):
            op = self.advance().value
            right = self.parse_factor()
            left = BinaryExpression(left, op, right)
        return left

  
    def parse_factor(self):
        token = self.current()

        if token.type == INTEGER:
            self.advance()
            return IntegerLiteral(token.value)

        elif token.type == IDENTIFIER:
            self.advance()
            return Identifier(token.value)

        elif token.type == LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(RPAREN)
            return expr

        else:
            raise ParseError(
                f"Unexpected token in expression: {token.type}('{token.value}')"
            )
