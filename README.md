# CSC321 – Language Implementation: Phase 1

A minimal lexer and parser for a statically typed, math-focused programming language.  
Phase 1 covers tokenization and AST construction — no evaluation or execution is performed.

---

## How to Run

Make sure you have **Python 3** installed. All source files are in the `src/` directory.

### Lex a file (tokenize)

```
python src/cli.py lex <file>
```

Example:
```
python src/cli.py lex tests/valid1.ml
```

Expected output:
```
IDENTIFIER(x)
EQUAL(=)
INTEGER(5)
SEMICOLON(;)
PRINT(print)
IDENTIFIER(x)
SEMICOLON(;)
EOF(EOF)
```

---

### Parse a file (build AST)

```
python src/cli.py parse <file>
```

Example:
```
python src/cli.py parse tests/valid1.ml
```

Expected output:
```
Program
  AssignmentStatement
    Identifier(x)
    IntegerLiteral(5)
  PrintStatement
    Identifier(x)
```

---

## Grammar (EBNF)

```
program       → statement* EOF
statement     → assignment | print_stmt
assignment    → IDENTIFIER '=' expression ';'
print_stmt    → 'print' expression ';'
expression    → term (('+' | '-') term)*
term          → factor (('*' | '/') factor)*
factor        → INTEGER | IDENTIFIER | '(' expression ')'
```

**Operator precedence** (highest to lowest):
1. Parentheses `()`
2. `*`, `/` — multiplication and division
3. `+`, `-` — addition and subtraction

All binary operators are **left-associative**.

---

## Architecture

```
src/
  lexer.py      — Tokenizes raw source text into a list of Token objects
  parser.py     — Recursive descent parser; consumes tokens and builds an AST
  ast_nodes.py  — AST node class definitions (Program, AssignmentStatement, etc.)
  cli.py        — Command-line interface; entry point for lex and parse commands
```

### Component Overview

**Lexer (`lexer.py`)**  
Scans the source string character by character. Skips whitespace, reads multi-character integers and identifiers, recognizes `print` as a keyword, and returns a flat list of `Token` objects ending with `EOF`. Unknown characters raise a `LexerError`.

**AST Nodes (`ast_nodes.py`)**  
Defines six node types as plain Python classes:
- `Program` — holds a list of statements
- `AssignmentStatement` — holds an `Identifier` and an expression
- `PrintStatement` — holds an expression
- `BinaryExpression` — holds left node, operator string, and right node
- `IntegerLiteral` — holds an integer value
- `Identifier` — holds a variable name string

**Parser (`parser.py`)**  
Recursive descent parser with three levels of precedence:
- `parse_expression` handles `+` and `-`
- `parse_term` handles `*` and `/`
- `parse_factor` handles literals, identifiers, and parenthesized expressions

Raises `ParseError` on any unexpected token. No error recovery is implemented.

**CLI (`cli.py`)**  
Reads the source file, runs the lexer, and (for `parse`) runs the parser and pretty-prints the AST as an indented tree.

---

## Test Cases

### Valid Programs (`tests/`)

| File | Description |
|---|---|
| `valid1.ml` | Simple assignment and print |
| `valid2.ml` | Arithmetic with operator precedence (`3 + 4 * 5`) |
| `valid3.ml` | Parentheses overriding precedence (`(3 + 4) * 5`) |
| `valid4.ml` | Two variables, one depends on the other |
| `valid5.ml` | Subtraction across two variables |
| `valid6.ml` | Left-associativity (`10 - 3 - 2`) |
| `valid7.ml` | Division then multiplication |
| `valid8.ml` | Deeply nested parentheses |
| `valid9.ml` | Multiple print statements |
| `valid10.ml`| Longer multi-variable program |

### Invalid Programs (`tests/`)

| File | Expected Error | Reason |
|---|---|---|
| `invalid1.ml` | Parse Error | Missing semicolon after assignment |
| `invalid2.ml` | Parse Error | Missing semicolon after print statement |
| `invalid3.ml` | Parse Error | Unmatched open parenthesis |
| `invalid4.ml` | Lexer Error | Unknown character `@` |
| `invalid5.ml` | Parse Error | `print` with no expression before `;` |

---

## What Is Not Supported in Phase 1

- No program execution or evaluation
- No variable storage or type checking
- No undefined variable detection
- No functions, loops, or conditionals
- No error recovery (first error stops the program)