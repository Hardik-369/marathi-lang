#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarathiLang Evaluator - Evaluates AST into executed statements
मराठी भाषा मूल्यांकन - AST चे विधानांत रूपांतर करा
"""

from typing import Any, Dict, List, Optional
from .parser import *
from .lexer import TokenType

class MarathiEvaluator:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, FunctionDefNode] = {}
        self.call_stack = []
        self.return_value = None

    def evaluate(self, node: ASTNode) -> Any:
        if isinstance(node, ProgramNode):
            result = None
            for statement in node.statements:
                result = self.evaluate(statement)
            return result

        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, BooleanNode):
            return node.value
        elif isinstance(node, NullNode):
            return None
        elif isinstance(node, IdentifierNode):
            if node.name not in self.variables:
                raise RuntimeError(f"Undefined variable '{node.name}'")
            return self.variables[node.name]

        elif isinstance(node, AssignmentNode):
            value = self.evaluate(node.value)
            if node.is_constant:
                if node.name in self.variables:
                    raise RuntimeError(f"Cannot reassign constant '{node.name}'")
            self.variables[node.name] = value
            return value

        elif isinstance(node, ArrayNode):
            return [self.evaluate(element) for element in node.elements]

        elif isinstance(node, IndexNode):
            array = self.evaluate(node.array)
            index = self.evaluate(node.index)
            if not isinstance(array, list):
                raise RuntimeError(f"Indexing non-array type")
            if not isinstance(index, int):
                raise RuntimeError(f"Array index must be an integer")
            if index < 0 or index >= len(array):
                raise RuntimeError(f"Array index out of bounds")
            return array[index]

        elif isinstance(node, BinaryOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            operator = node.operator
            if operator == '+':
                return left + right
            elif operator == '-':
                return left - right
            elif operator == '*':
                return left * right
            elif operator == '/':
                if right == 0:
                    raise RuntimeError("Division by zero")
                return left / right
            elif operator == '%':
                return left % right
            elif operator == '==':
                return left == right
            elif operator == '!=':
                return left != right
            elif operator == '<':
                return left < right
            elif operator == '>':
                return left > right
            elif operator == '<=':
                return left <= right
            elif operator == '>=':
                return left >= right
            elif operator == 'आणि':
                return left and right
            elif operator == 'किंवा':
                return left or right
            else:
                raise RuntimeError(f"Unknown binary operator: {operator}")

        elif isinstance(node, UnaryOpNode):
            operand = self.evaluate(node.operand)
            operator = node.operator
            if operator == 'नाही':
                return not operand
            elif operator == '-':
                return -operand

        elif isinstance(node, PrintNode):
            arguments = [self.evaluate(arg) for arg in node.arguments]
            try:
                print(*arguments)
            except UnicodeEncodeError:
                # Handle Unicode encoding issues
                import sys
                output = ' '.join(str(arg) for arg in arguments)
                sys.stdout.buffer.write(output.encode('utf-8'))
                sys.stdout.buffer.write(b'\n')
                sys.stdout.buffer.flush()

        elif isinstance(node, IfNode):
            condition = self.evaluate(node.condition)
            if condition:
                for stmt in node.then_branch:
                    result = self.evaluate(stmt)
                    if isinstance(stmt, ReturnNode):
                        return result
            elif node.else_branch:
                for stmt in node.else_branch:
                    result = self.evaluate(stmt)
                    if isinstance(stmt, ReturnNode):
                        return result

        elif isinstance(node, WhileNode):
            while self.evaluate(node.condition):
                for stmt in node.body:
                    self.evaluate(stmt)

        elif isinstance(node, ForEachNode):
            iterable = self.evaluate(node.iterable)
            if not isinstance(iterable, list):
                raise RuntimeError("ForEach expects a list")
            for element in iterable:
                self.variables[node.variable] = element
                for stmt in node.body:
                    self.evaluate(stmt)

        elif isinstance(node, FunctionDefNode):
            self.functions[node.name] = node

        elif isinstance(node, FunctionCallNode):
            function = self.functions.get(node.name)
            if not function:
                raise RuntimeError(f"अपरिभाषित कार्य '{node.name}'")

            arguments = [self.evaluate(arg) for arg in node.arguments]
            return self.execute_function(function, arguments)
        
        elif isinstance(node, ReturnNode):
            if node.value:
                return self.evaluate(node.value)
            return None

    def execute_function(self, function: FunctionDefNode, arguments: List[Any]) -> Any:
        # Save previous state
        previous_variables = self.variables.copy()
        previous_return = self.return_value
        self.return_value = None

        if len(function.parameters) != len(arguments):
            raise RuntimeError("Argument count mismatch")

        # Set up parameters
        for param, arg in zip(function.parameters, arguments):
            self.variables[param] = arg

        # Execute function body
        try:
            for stmt in function.body:
                if isinstance(stmt, ReturnNode):
                    if stmt.value:
                        self.return_value = self.evaluate(stmt.value)
                    else:
                        self.return_value = None
                    break
                else:
                    result = self.evaluate(stmt)
                    # Check if we encountered a return statement in nested structure
                    if isinstance(stmt, IfNode) and result is not None:
                        self.return_value = result
                        break
        except Exception as e:
            # Restore state on error
            self.variables = previous_variables
            self.return_value = previous_return
            raise e

        # Get return value
        result = self.return_value
        
        # Restore state
        self.variables = previous_variables
        self.return_value = previous_return
        
        return result

    def get_variables(self) -> Dict[str, Any]:
        return self.variables

    def load_module(self, name: str, module: Any):
        self.variables[name] = module

# Test the evaluator
if __name__ == "__main__":
    from lexer import MarathiLexer
    from parser import MarathiParser

    lexer = MarathiLexer()
    parser = MarathiParser()
    evaluator = MarathiEvaluator()

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

    print("\nEvaluation:")
    evaluator.evaluate(ast)
