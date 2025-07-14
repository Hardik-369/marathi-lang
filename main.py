#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarathiLang - A Marathi-inspired programming language
मराठी भाषा - मराठी-प्रेरित प्रोग्रामिंग भाषा

Main entry point for the interpreter
"""

import sys
import os
import argparse
from pathlib import Path
import io

# Fix Unicode encoding issues on Windows
if sys.platform == 'win32':
    # Set console to UTF-8 mode
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)
    except:
        pass

# Add interpreter directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'interpreter'))

from interpreter.lexer import MarathiLexer
from interpreter.parser import MarathiParser
from interpreter.evaluator import MarathiEvaluator
from interpreter.stdlib.ganit import GanitModule
from interpreter.stdlib.shabd import ShabdModule
from interpreter.stdlib.pravesh import PraveshModule

class MarathiREPL:
    def __init__(self):
        self.lexer = MarathiLexer()
        self.parser = MarathiParser()
        self.evaluator = MarathiEvaluator()
        self.history = []
        
        # Load standard library modules
        self.evaluator.load_module('गणित', GanitModule())
        self.evaluator.load_module('शब्द', ShabdModule())
        self.evaluator.load_module('प्रवेश', PraveshModule())
        
    def run_repl(self):
        print("मराठी भाषा v1.0 - Marathi Programming Language")
        print("मदत टाइप करा किंवा 'help' टाइप करा")
        print("बाहेर जाण्यासाठी 'बाहेर' टाइप करा")
        print("-" * 50)
        
        while True:
            try:
                line = input("मराठी>>> ")
                
                if not line.strip():
                    continue
                    
                # Handle REPL commands
                if line.strip() in ['बाहेर', 'exit']:
                    print("धन्यवाद! Goodbye!")
                    break
                elif line.strip() in ['मदत', 'help']:
                    self.show_help()
                    continue
                elif line.strip() == 'इतिहास':
                    self.show_history()
                    continue
                elif line.strip() == 'चल':
                    self.show_variables()
                    continue
                elif line.strip() == 'दस्त':
                    self.show_documentation()
                    continue
                elif line.strip().startswith('उदाहरण'):
                    topic = line.strip().split()[1] if len(line.strip().split()) > 1 else None
                    self.show_example(topic)
                    continue
                
                # Add to history
                self.history.append(line)
                
                # Execute code
                self.execute_line(line)
                
            except KeyboardInterrupt:
                print("\nKeyboard interrupt. बाहेर जाण्यासाठी 'बाहेर' टाइप करा")
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"त्रुटी: {e}")
    
    def execute_line(self, line):
        try:
            tokens = self.lexer.tokenize(line)
            ast = self.parser.parse(tokens)
            result = self.evaluator.evaluate(ast)
            
            if result is not None:
                print(result)
                
        except Exception as e:
            try:
                print(f"त्रुटी: {e}")
            except UnicodeEncodeError:
                print(f"Error: {e}")
    
    def execute_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tokens = self.lexer.tokenize(code)
            ast = self.parser.parse(tokens)
            self.evaluator.evaluate(ast)
            
        except FileNotFoundError:
            try:
                print(f"त्रुटी: फाइल '{filename}' सापडली नाही")
            except UnicodeEncodeError:
                print(f"Error: File '{filename}' not found")
        except Exception as e:
            try:
                print(f"त्रुटी: {e}")
            except UnicodeEncodeError:
                print(f"Error: {e}")
    
    def show_help(self):
        help_text = """
मराठी भाषा - मदत (MarathiLang Help)
==========================================

मुख्य आज्ञा (Basic Commands):
- मुद्रण("मजकूर") - Print text
- चल नाव = मूल्य - Declare variable
- स्थिर नाव = मूल्य - Declare constant
- कार्य नाव() { ... } - Define function

प्रकार (Data Types):
- संख्या: १, २, ३.१४
- शब्द: "नमस्कार"
- सत्य/असत्य (Boolean)
- शून्य (null)

नियंत्रण संरचना (Control Structures):
- जर ... { } नाहीतर { } - If-else
- जोपर्यंत ... { } - While loop
- प्रत्येक ... मध्ये ... { } - For each loop

REPL आज्ञा (REPL Commands):
- मदत - Show this help
- बाहेर - Exit
- इतिहास - Show command history
- चल - Show variables
- दस्त - Show documentation
- उदाहरण [topic] - Show example
        """
        print(help_text)
    
    def show_history(self):
        print("इतिहास (Command History):")
        for i, cmd in enumerate(self.history, 1):
            print(f"{i}: {cmd}")
    
    def show_variables(self):
        print("चल (Variables):")
        for name, value in self.evaluator.get_variables().items():
            print(f"{name} = {value}")
    
    def show_documentation(self):
        print("दस्तावेज (Documentation) - मराठी भाषा")
        print("पूर्ण दस्तावेज docs/मराठी_डॉक.md मध्ये पाहा")
    
    def show_example(self, topic=None):
        examples = {
            'hello': '''
उदाहरण - नमस्कार (Hello Example):
कार्य नमस्कार() {
    मुद्रण("नमस्कार जग!")
}
नमस्कार()
            ''',
            'variables': '''
उदाहरण - चल (Variables Example):
चल नाव = "राम"
चल वय = २५
स्थिर pi = ३.१४
मुद्रण(नाव, वय)
            ''',
            'loops': '''
उदाहरण - पुनरावृत्ती (Loops Example):
चल i = १
जोपर्यंत i <= ५ {
    मुद्रण(i)
    i = i + १
}
            '''
        }
        
        if topic and topic in examples:
            print(examples[topic])
        else:
            print("उपलब्ध उदाहरणे: hello, variables, loops")

def main():
    parser = argparse.ArgumentParser(description='मराठी भाषा - Marathi Programming Language')
    parser.add_argument('file', nargs='?', help='MarathiLang file to execute (.mr)')
    parser.add_argument('--repl', action='store_true', help='Start REPL mode')
    parser.add_argument('--version', action='version', version='मराठी भाषा 1.0')
    
    args = parser.parse_args()
    
    repl = MarathiREPL()
    
    if args.file:
        repl.execute_file(args.file)
    else:
        repl.run_repl()

if __name__ == '__main__':
    main()
