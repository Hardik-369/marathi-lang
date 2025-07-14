#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarathiLang Lexer - Tokenizes Marathi code into tokens
मराठी भाषा लेक्सर - मराठी कोड टोकन्समध्ये रूपांतरित करतो
"""

import re
import unicodedata
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Any

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NULL = auto()
    
    # Identifiers and Keywords
    IDENTIFIER = auto()
    
    # Variable/Function Keywords
    CHAL = auto()        # चल (variable)
    STHIR = auto()       # स्थिर (constant)
    KARYA = auto()       # कार्य (function)
    PARAT = auto()       # परत (return)
    
    # Control Flow
    JAR = auto()         # जर (if)
    NAHITAR = auto()     # नाहीतर (else)
    JOPARYANT = auto()   # जोपर्यंत (while)
    PRATYEKA = auto()    # प्रत्येक (for each)
    MADHYE = auto()      # मध्ये (in)
    
    # Built-in Functions
    MUDRAN = auto()      # मुद्रण (print)
    PRAKAAR = auto()     # प्रकार (type)
    LAMBI = auto()       # लांबी (length)
    SANKHYA = auto()     # संख्या (number cast)
    SHUSHOBHIT = auto()  # सुशोभित (string cast)
    
    # Operators
    ASSIGN = auto()      # =
    PLUS = auto()        # +
    MINUS = auto()       # -
    MULTIPLY = auto()    # *
    DIVIDE = auto()      # /
    MODULO = auto()      # %
    
    # Comparison
    EQUAL = auto()       # ==
    NOT_EQUAL = auto()   # !=
    LESS = auto()        # <
    GREATER = auto()     # >
    LESS_EQUAL = auto()  # <=
    GREATER_EQUAL = auto() # >=
    
    # Logical
    ANI = auto()         # आणि (and)
    KINVA = auto()       # किंवा (or)
    NAHI = auto()        # नाही (not)
    
    # Punctuation
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    COMMA = auto()       # ,
    SEMICOLON = auto()   # ;
    NEWLINE = auto()     # \n
    
    # Special
    EOF = auto()
    UNKNOWN = auto()

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

class MarathiLexer:
    def __init__(self):
        # Marathi keywords mapping
        self.keywords = {
            'चल': TokenType.CHAL,
            'स्थिर': TokenType.STHIR,
            'कार्य': TokenType.KARYA,
            'परत': TokenType.PARAT,
            'जर': TokenType.JAR,
            'नाहीतर': TokenType.NAHITAR,
            'जोपर्यंत': TokenType.JOPARYANT,
            'प्रत्येक': TokenType.PRATYEKA,
            'मध्ये': TokenType.MADHYE,
            'मुद्रण': TokenType.MUDRAN,
            'प्रकार': TokenType.PRAKAAR,
            'लांबी': TokenType.LAMBI,
            'संख्या': TokenType.SANKHYA,
            'सुशोभित': TokenType.SHUSHOBHIT,
            'आणि': TokenType.ANI,
            'किंवा': TokenType.KINVA,
            'नाही': TokenType.NAHI,
            'सत्य': TokenType.BOOLEAN,
            'असत्य': TokenType.BOOLEAN,
            'शून्य': TokenType.NULL,
        }
        
        # Marathi numerals to Arabic numerals mapping
        self.marathi_to_arabic = {
            '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
            '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
        }
        
        self.arabic_to_marathi = {v: k for k, v in self.marathi_to_arabic.items()}
        
        # Token patterns
        self.token_patterns = [
            # Comments (ignore)
            (r'//.*$', None),
            (r'/\*.*?\*/', None),
            
            # Numbers (Marathi and Arabic)
            (r'[०-९]+(\.[०-९]+)?', 'MARATHI_NUMBER'),
            (r'[0-9]+(\.[0-9]+)?', 'ARABIC_NUMBER'),
            
            # Strings
            (r'"[^"]*"', 'STRING'),
            (r"'[^']*'", 'STRING'),
            
            # Two-character operators
            (r'==', 'EQUAL'),
            (r'!=', 'NOT_EQUAL'),
            (r'<=', 'LESS_EQUAL'),
            (r'>=', 'GREATER_EQUAL'),
            
            # Single-character operators
            (r'=', 'ASSIGN'),
            (r'\+', 'PLUS'),
            (r'-', 'MINUS'),
            (r'\*', 'MULTIPLY'),
            (r'/', 'DIVIDE'),
            (r'%', 'MODULO'),
            (r'<', 'LESS'),
            (r'>', 'GREATER'),
            
            # Punctuation
            (r'\(', 'LPAREN'),
            (r'\)', 'RPAREN'),
            (r'\{', 'LBRACE'),
            (r'\}', 'RBRACE'),
            (r'\[', 'LBRACKET'),
            (r'\]', 'RBRACKET'),
            (r',', 'COMMA'),
            (r';', 'SEMICOLON'),
            (r'\n', 'NEWLINE'),
            
            # Identifiers and keywords (Devanagari and English)
            (r'[अ-ह्][अ-ह्ा-ृॆ-ौं-्०-९]*', 'IDENTIFIER'),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),
            
            # Skip whitespace (except newlines)
            (r'[ \t]+', None),
        ]
        
        # Compile patterns
        self.compiled_patterns = [
            (re.compile(pattern, re.MULTILINE), token_type)
            for pattern, token_type in self.token_patterns
        ]
    
    def convert_marathi_number(self, marathi_num: str) -> str:
        """Convert Marathi numerals to Arabic numerals"""
        arabic_num = ""
        for char in marathi_num:
            if char in self.marathi_to_arabic:
                arabic_num += self.marathi_to_arabic[char]
            else:
                arabic_num += char
        return arabic_num
    
    def tokenize(self, text: str) -> List[Token]:
        """Tokenize the input text into a list of tokens"""
        tokens = []
        line = 1
        column = 1
        pos = 0
        
        while pos < len(text):
            match_found = False
            
            for pattern, token_type in self.compiled_patterns:
                match = pattern.match(text, pos)
                if match:
                    value = match.group(0)
                    
                    # Skip if token_type is None (comments, whitespace)
                    if token_type is None:
                        pass
                    elif token_type == 'NEWLINE':
                        tokens.append(Token(TokenType.NEWLINE, value, line, column))
                        line += 1
                        column = 1
                    elif token_type == 'MARATHI_NUMBER':
                        arabic_value = self.convert_marathi_number(value)
                        numeric_value = float(arabic_value) if '.' in arabic_value else int(arabic_value)
                        tokens.append(Token(TokenType.NUMBER, numeric_value, line, column))
                    elif token_type == 'ARABIC_NUMBER':
                        numeric_value = float(value) if '.' in value else int(value)
                        tokens.append(Token(TokenType.NUMBER, numeric_value, line, column))
                    elif token_type == 'STRING':
                        string_value = value[1:-1]  # Remove quotes
                        tokens.append(Token(TokenType.STRING, string_value, line, column))
                    elif token_type == 'IDENTIFIER':
                        # Check if it's a keyword
                        if value in self.keywords:
                            if value in ['सत्य', 'असत्य']:
                                boolean_value = value == 'सत्य'
                                tokens.append(Token(TokenType.BOOLEAN, boolean_value, line, column))
                            elif value == 'शून्य':
                                tokens.append(Token(TokenType.NULL, None, line, column))
                            else:
                                tokens.append(Token(self.keywords[value], value, line, column))
                        else:
                            tokens.append(Token(TokenType.IDENTIFIER, value, line, column))
                    else:
                        # Map string token types to enum values
                        token_type_enum = getattr(TokenType, token_type, TokenType.UNKNOWN)
                        tokens.append(Token(token_type_enum, value, line, column))
                    
                    pos = match.end()
                    column += len(value)
                    match_found = True
                    break
            
            if not match_found:
                # Unknown character
                char = text[pos]
                tokens.append(Token(TokenType.UNKNOWN, char, line, column))
                pos += 1
                column += 1
        
        # Add EOF token
        tokens.append(Token(TokenType.EOF, None, line, column))
        return tokens
    
    def format_tokens(self, tokens: List[Token]) -> str:
        """Format tokens for debugging"""
        result = []
        for token in tokens:
            if token.type == TokenType.EOF:
                break
            result.append(f"{token.type.name}: {repr(token.value)}")
        return "\n".join(result)

# Test the lexer
if __name__ == "__main__":
    lexer = MarathiLexer()
    
    # Test code
    test_code = '''
    चल नाव = "राम"
    चल वय = २५
    स्थिर pi = ३.१४
    
    कार्य नमस्कार(कोण) {
        मुद्रण("नमस्कार", कोण)
        परत सत्य
    }
    
    जर वय >= १८ {
        मुद्रण("प्रौढ")
    } नाहीतर {
        मुद्रण("अल्पवयीन")
    }
    '''
    
    tokens = lexer.tokenize(test_code)
    print(lexer.format_tokens(tokens))
