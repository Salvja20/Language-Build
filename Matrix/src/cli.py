import sys
import os


sys.path.insert(0, os.path.dirname(__file__))

from lexer import Lexer, LexerError
from parser import Parser, ParseError
from ast_nodes import (
    Program, AssignmentStatement, PrintStatement,
    BinaryExpression, IntegerLiteral, Identifier
)


def print_ast(node, indent=0):
    pad = "  " * indent
    if isinstance(node, Program):
        print(f"{pad}Program")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)

    elif isinstance(node, AssignmentStatement):
        print(f"{pad}AssignmentStatement")
        print_ast(node.identifier, indent + 1)
        print_ast(node.expression, indent + 1)

    elif isinstance(node, PrintStatement):
        print(f"{pad}PrintStatement")
        print_ast(node.expression, indent + 1)

    elif isinstance(node, BinaryExpression):
        print(f"{pad}BinaryExpression({node.operator})")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)

    elif isinstance(node, IntegerLiteral):
        print(f"{pad}IntegerLiteral({node.value})")

    elif isinstance(node, Identifier):
        print(f"{pad}Identifier({node.name})")

    else:
        print(f"{pad}Unknown({node})")


def main():
    if len(sys.argv) != 3:
        print("Usage: python cli.py [lex|parse] <file>")
        sys.exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    try:
        with open(filename, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    
    if command == 'lex':
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            for token in tokens:
                print(token)
        except LexerError as e:
            print(f"Lexer Error: {e}")
            sys.exit(1)

   
    elif command == 'parse':
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse_program()
            print_ast(ast)
        except LexerError as e:
            print(f"Lexer Error: {e}")
            sys.exit(1)
        except ParseError as e:
            print(f"Parse Error: {e}")
            sys.exit(1)

    else:
        print(f"Unknown command '{command}'. Use 'lex' or 'parse'.")
        sys.exit(1)


if __name__ == '__main__':
    main()
