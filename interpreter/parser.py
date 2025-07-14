#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarathiLang Parser - Generates AST from tokens
मराठी भाषा पार्सर - टोकन्समधून AST तयार करतो
"""

from typing import List, Optional, Union
from dataclasses import dataclass
from .lexer import Token, TokenType

# AST Node Classes
@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    pass

@dataclass
class NumberNode(ASTNode):
    value: Union[int, float]

@dataclass
class StringNode(ASTNode):
    value: str

@dataclass
class BooleanNode(ASTNode):
    value: bool

@dataclass
class NullNode(ASTNode):
    pass

@dataclass
class IdentifierNode(ASTNode):
    name: str

@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class UnaryOpNode(ASTNode):
    operator: str
    operand: ASTNode

@dataclass
class AssignmentNode(ASTNode):
    name: str
    value: ASTNode
    is_constant: bool = False

@dataclass
class FunctionDefNode(ASTNode):
    name: str
    parameters: List[str]
    body: List[ASTNode]

@dataclass
class FunctionCallNode(ASTNode):
    name: str
    arguments: List[ASTNode]

@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: Optional[List[ASTNode]] = None

@dataclass
class WhileNode(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

@dataclass
class ForEachNode(ASTNode):
    variable: str
    iterable: ASTNode
    body: List[ASTNode]

@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode] = None

@dataclass
class PrintNode(ASTNode):
    arguments: List[ASTNode]

@dataclass
class ArrayNode(ASTNode):
    elements: List[ASTNode]

@dataclass
class IndexNode(ASTNode):
    array: ASTNode
    index: ASTNode

@dataclass
class BreakNode(ASTNode):
    pass

@dataclass
class ContinueNode(ASTNode):
    pass

@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]

class MarathiParser:
    def __init__(self):
        self.tokens = []
        self.current = 0
    
    def parse(self, tokens: List[Token]) -> ProgramNode:
        """Parse tokens into an AST"""
        self.tokens = tokens
        self.current = 0
        
        statements = []
        while not self.is_at_end():
            # Skip newlines
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        
        return ProgramNode(statements)
    
    def statement(self) -> Optional[ASTNode]:
        """Parse a statement"""
        try:
            if self.match(TokenType.CHAL):
                return self.variable_declaration(is_constant=False)
            elif self.match(TokenType.STHIR):
                return self.variable_declaration(is_constant=True)
            elif self.match(TokenType.KARYA):
                return self.function_declaration()
            elif self.match(TokenType.JAR):
                return self.if_statement()
            elif self.match(TokenType.JOPARYANT):
                return self.while_statement()
            elif self.match(TokenType.PRATYEKA):
                return self.for_each_statement()
            elif self.match(TokenType.PARAT):
                return self.return_statement()
            elif self.match(TokenType.MUDRAN):
                return self.print_statement()
            else:
                return self.expression_statement()
        except Exception as e:
            print(f"व्याकरण त्रुटी: {e}")
            # Skip to next statement by advancing to next newline or EOF
            while not self.check(TokenType.NEWLINE) and not self.is_at_end():
                self.advance()
            return None
    
    def variable_declaration(self, is_constant: bool) -> AssignmentNode:
        """Parse variable declaration"""
        name = self.consume(TokenType.IDENTIFIER, "चल नावाची अपेक्षा").value
        self.consume(TokenType.ASSIGN, "'=' ची अपेक्षा")
        value = self.expression()
        return AssignmentNode(name, value, is_constant)
    
    def function_declaration(self) -> FunctionDefNode:
        """Parse function declaration"""
        name = self.consume(TokenType.IDENTIFIER, "कार्य नावाची अपेक्षा").value
        
        self.consume(TokenType.LPAREN, "'(' ची अपेक्षा")
        parameters = []
        
        if not self.check(TokenType.RPAREN):
            parameters.append(self.consume(TokenType.IDENTIFIER, "पॅरामीटर नावाची अपेक्षा").value)
            while self.match(TokenType.COMMA):
                parameters.append(self.consume(TokenType.IDENTIFIER, "पॅरामीटर नावाची अपेक्षा").value)
        
        self.consume(TokenType.RPAREN, "')' ची अपेक्षा")
        self.consume(TokenType.LBRACE, "'{' ची अपेक्षा")
        
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        
        self.consume(TokenType.RBRACE, "'}' ची अपेक्षा")
        return FunctionDefNode(name, parameters, body)
    
    def if_statement(self) -> IfNode:
        """Parse if statement"""
        condition = self.expression()
        self.consume(TokenType.LBRACE, "'{' ची अपेक्षा")
        
        then_branch = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            stmt = self.statement()
            if stmt:
                then_branch.append(stmt)
        
        self.consume(TokenType.RBRACE, "'}' ची अपेक्षा")
        
        else_branch = None
        if self.match(TokenType.NAHITAR):
            self.consume(TokenType.LBRACE, "'{' ची अपेक्षा")
            else_branch = []
            while not self.check(TokenType.RBRACE) and not self.is_at_end():
                if self.check(TokenType.NEWLINE):
                    self.advance()
                    continue
                stmt = self.statement()
                if stmt:
                    else_branch.append(stmt)
            self.consume(TokenType.RBRACE, "'}' ची अपेक्षा")
        
        return IfNode(condition, then_branch, else_branch)
    
    def while_statement(self) -> WhileNode:
        """Parse while statement"""
        condition = self.expression()
        self.consume(TokenType.LBRACE, "'{' ची अपेक्षा")
        
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        
        self.consume(TokenType.RBRACE, "'}' ची अपेक्षा")
        return WhileNode(condition, body)
    
    def for_each_statement(self) -> ForEachNode:
        """Parse for each statement"""
        # Handle variable name - can be identifier or certain keywords used as identifiers
        if self.check(TokenType.IDENTIFIER):
            variable = self.advance().value
        elif self.check(TokenType.SANKHYA):  # Allow संख्या as variable name
            variable = self.advance().value
        else:
            raise RuntimeError("चल नावाची अपेक्षा")
        
        self.consume(TokenType.MADHYE, "'मध्ये' ची अपेक्षा")
        iterable = self.expression()
        self.consume(TokenType.LBRACE, "'{' ची अपेक्षा")
        
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        
        self.consume(TokenType.RBRACE, "'}' ची अपेक्षा")
        return ForEachNode(variable, iterable, body)
    
    def return_statement(self) -> ReturnNode:
        """Parse return statement"""
        value = None
        if not self.check(TokenType.NEWLINE) and not self.is_at_end():
            value = self.expression()
        return ReturnNode(value)
    
    def print_statement(self) -> PrintNode:
        """Parse print statement"""
        if not self.check(TokenType.LPAREN):
            raise RuntimeError("print statement requires '(' after मुद्रण")
        
        self.consume(TokenType.LPAREN, "'(' ची अपेक्षा")
        arguments = []
        
        if not self.check(TokenType.RPAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.expression())
        
        self.consume(TokenType.RPAREN, "')' ची अपेक्षा")
        return PrintNode(arguments)
    
    def expression_statement(self) -> ASTNode:
        """Parse expression statement"""
        expr = self.expression()
        
        # Check for assignment
        if isinstance(expr, IdentifierNode) and self.check(TokenType.ASSIGN):
            self.advance()  # consume '='
            value = self.expression()
            return AssignmentNode(expr.name, value, False)
        
        # Skip semicolons if present
        if self.check(TokenType.SEMICOLON):
            self.advance()
        return expr
    
    def expression(self) -> ASTNode:
        """Parse expression"""
        return self.logical_or()
    
    def logical_or(self) -> ASTNode:
        """Parse logical OR expression"""
        expr = self.logical_and()
        
        while self.match(TokenType.KINVA):
            operator = self.previous().value
            right = self.logical_and()
            expr = BinaryOpNode(expr, operator, right)
        
        return expr
    
    def logical_and(self) -> ASTNode:
        """Parse logical AND expression"""
        expr = self.equality()
        
        while self.match(TokenType.ANI):
            operator = self.previous().value
            right = self.equality()
            expr = BinaryOpNode(expr, operator, right)
        
        return expr
    
    def equality(self) -> ASTNode:
        """Parse equality expression"""
        expr = self.comparison()
        
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self.previous().value
            right = self.comparison()
            expr = BinaryOpNode(expr, operator, right)
        
        return expr
    
    def comparison(self) -> ASTNode:
        """Parse comparison expression"""
        expr = self.term()
        
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous().value
            right = self.term()
            expr = BinaryOpNode(expr, operator, right)
        
        return expr
    
    def term(self) -> ASTNode:
        """Parse term expression"""
        expr = self.factor()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().value
            right = self.factor()
            expr = BinaryOpNode(expr, operator, right)
        
        return expr
    
    def factor(self) -> ASTNode:
        """Parse factor expression"""
        expr = self.unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.previous().value
            right = self.unary()
            expr = BinaryOpNode(expr, operator, right)
        
        return expr
    
    def unary(self) -> ASTNode:
        """Parse unary expression"""
        if self.match(TokenType.NAHI, TokenType.MINUS):
            operator = self.previous().value
            right = self.unary()
            return UnaryOpNode(operator, right)
        
        return self.call()
    
    def call(self) -> ASTNode:
        """Parse function call and array indexing"""
        expr = self.primary()
        
        while True:
            if self.match(TokenType.LPAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.LBRACKET):
                index = self.expression()
                self.consume(TokenType.RBRACKET, "']' ची अपेक्षा")
                expr = IndexNode(expr, index)
            else:
                break
        
        return expr
    
    def finish_call(self, callee: ASTNode) -> FunctionCallNode:
        """Finish parsing function call"""
        arguments = []
        
        if not self.check(TokenType.RPAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.expression())
        
        self.consume(TokenType.RPAREN, "')' ची अपेक्षा")
        
        if isinstance(callee, IdentifierNode):
            return FunctionCallNode(callee.name, arguments)
        else:
            raise RuntimeError("अवैध कार्य कॉल")
    
    def primary(self) -> ASTNode:
        """Parse primary expression"""
        if self.match(TokenType.BOOLEAN):
            return BooleanNode(self.previous().value)
        
        if self.match(TokenType.NULL):
            return NullNode()
        
        if self.match(TokenType.NUMBER):
            return NumberNode(self.previous().value)
        
        if self.match(TokenType.STRING):
            return StringNode(self.previous().value)
        
        if self.match(TokenType.IDENTIFIER):
            return IdentifierNode(self.previous().value)
        
        if self.match(TokenType.LBRACKET):
            return self.array_literal()
        
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "')' ची अपेक्षा")
            return expr
        
        raise RuntimeError(f"अनपेक्षित टोकन: {self.peek().value}")
    
    def array_literal(self) -> ArrayNode:
        """Parse array literal [1, 2, 3]"""
        elements = []
        
        if not self.check(TokenType.RBRACKET):
            elements.append(self.expression())
            while self.match(TokenType.COMMA):
                elements.append(self.expression())
        
        self.consume(TokenType.RBRACKET, "']' ची अपेक्षा")
        return ArrayNode(elements)
    
    # Helper methods
    def match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    def check(self, token_type: TokenType) -> bool:
        """Check if current token is of given type"""
        if self.is_at_end():
            return False
        return self.peek().type == token_type
    
    def advance(self) -> Token:
        """Consume current token and return it"""
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self) -> bool:
        """Check if we're at the end of tokens"""
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        """Return current token without consuming it"""
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        """Return previous token"""
        return self.tokens[self.current - 1]
    
    def consume(self, token_type: TokenType, message: str) -> Token:
        """Consume token of given type or raise error"""
        if self.check(token_type):
            return self.advance()
        
        current_token = self.peek()
        raise RuntimeError(f"{message}. मिळाले: {current_token.value} ({current_token.line}:{current_token.column})")

# Test the parser
if __name__ == "__main__":
    from lexer import MarathiLexer
    
    lexer = MarathiLexer()
    parser = MarathiParser()
    
    # Test code
    test_code = '''
    चल नाव = "राम"
    मुद्रण(नाव)
    '''
    
    tokens = lexer.tokenize(test_code)
    print("Tokens:")
    print(lexer.format_tokens(tokens))
    
    print("\nAST:")
    ast = parser.parse(tokens)
    print(ast)
