# मराठी भाषा (Marathi Programming Language)

A programming language inspired by Marathi, designed to make programming accessible to Marathi speakers.

## Features

- **Marathi Keywords**: Uses Marathi words for programming constructs
- **Unicode Support**: Full support for Devanagari script
- **GUI IDE**: Built-in graphical interface for coding
- **REPL Mode**: Interactive programming environment
- **Standard Library**: Built-in modules for common operations

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.7+ installed
3. Install required dependencies:
   ```bash
   pip install tkinter
   ```

## Usage

### Running the GUI IDE

```bash
python marathi_ide.py
```

### Running Marathi Files

```bash
python run_marathi.py filename.mr
```

### REPL Mode

```bash
python main.py
```

## Language Syntax

### Basic Syntax

#### Variables and Constants
```marathi
चल नाव = "राम"          // Variable declaration
स्थिर PI = ३.१४          // Constant declaration
```

#### Data Types
```marathi
चल संख्या = १०           // Number (Marathi numerals)
चल संख्या = 10           // Number (Arabic numerals)
चल शब्द = "नमस्कार"      // String
चल बूलियन = सत्य         // Boolean (true)
चल बूलियन = असत्य        // Boolean (false)
चल रिक्त = शून्य          // Null
चल यादी = [१, २, ३]       // Array
```

#### Print Statement
```marathi
मुद्रण("नमस्कार जग!")     // Print statement
मुद्रण("नाव:", नाव)       // Print with variables
```

#### Functions
```marathi
कार्य वर्ग(x) {
    परत x * x
}

कार्य नमस्कार(नाव) {
    मुद्रण("नमस्कार", नाव)
}
```

#### Control Flow

##### If-Else
```marathi
जर वय >= १८ {
    मुद्रण("प्रौढ")
} नाहीतर {
    मुद्रण("अल्पवयीन")
}
```

##### While Loop
```marathi
चल i = १
जोपर्यंत i <= ५ {
    मुद्रण("संख्या:", i)
    i = i + १
}
```

##### For-Each Loop
```marathi
चल यादी = [१, २, ३, ४, ५]
प्रत्येक item मध्ये यादी {
    मुद्रण("आयटम:", item)
}
```

#### Operators

##### Arithmetic
- `+` (addition)
- `-` (subtraction)
- `*` (multiplication)
- `/` (division)
- `%` (modulo)

##### Comparison
- `==` (equal)
- `!=` (not equal)
- `<` (less than)
- `>` (greater than)
- `<=` (less than or equal)
- `>=` (greater than or equal)

##### Logical
- `आणि` (and)
- `किंवा` (or)
- `नाही` (not)

### Keywords Reference

| Marathi | English | Description |
|---------|---------|-------------|
| चल | var | Variable declaration |
| स्थिर | const | Constant declaration |
| कार्य | function | Function declaration |
| परत | return | Return statement |
| जर | if | If statement |
| नाहीतर | else | Else statement |
| जोपर्यंत | while | While loop |
| प्रत्येक | foreach | For-each loop |
| मध्ये | in | In operator |
| मुद्रण | print | Print statement |
| सत्य | true | Boolean true |
| असत्य | false | Boolean false |
| शून्य | null | Null value |
| आणि | and | Logical AND |
| किंवा | or | Logical OR |
| नाही | not | Logical NOT |

## Examples

### Hello World
```marathi
मुद्रण("नमस्कार जग!")
```

### Fibonacci Sequence
```marathi
कार्य फिबो(n) {
    जर n <= १ {
        परत n
    }
    परत फिबो(n - १) + फिबो(n - २)
}

चल परिणाम = फिबो(८)
मुद्रण("फिबोनाची संख्या:", परिणाम)
```

### Factorial
```marathi
कार्य फॅक्टोरियल(n) {
    जर n <= १ {
        परत १
    }
    परत n * फॅक्टोरियल(n - १)
}

मुद्रण("फॅक्टोरियल:", फॅक्टोरियल(५))
```

### Array Operations
```marathi
चल यादी = [१, २, ३, ४, ५]
मुद्रण("यादी:", यादी)
मुद्रण("पहिला element:", यादी[०])

प्रत्येक num मध्ये यादी {
    मुद्रण("संख्या:", num)
}
```

## GUI IDE Features

The built-in IDE (`marathi_ide.py`) provides:

- **Code Editor**: Syntax-highlighted text editor
- **Run Code**: Execute Marathi programs with F5 or Run button
- **File Operations**: New, Open, Save files
- **Output Display**: Shows program output and errors
- **Status Bar**: Shows current operation status
- **Keyboard Shortcuts**:
  - `F5` or `Ctrl+R`: Run code
  - `Ctrl+N`: New file
  - `Ctrl+O`: Open file
  - `Ctrl+S`: Save file

## REPL Commands

When running in REPL mode:
- `मदत` or `help`: Show help
- `बाहेर` or `exit`: Exit REPL
- `इतिहास`: Show command history
- `चल`: Show variables
- `दस्त`: Show documentation
- `उदाहरण [topic]`: Show examples

## File Structure

```
marathi-lang/
├── main.py                    # Main interpreter entry point
├── run_marathi.py            # Unicode-safe wrapper script
├── marathi_ide.py            # GUI IDE
├── interpreter/
│   ├── __init__.py
│   ├── lexer.py              # Tokenizer
│   ├── parser.py             # Parser (AST generation)
│   ├── evaluator.py          # Evaluator (execution)
│   └── stdlib/               # Standard library
│       ├── __init__.py
│       ├── ganit.py          # Math module
│       ├── shabd.py          # String module
│       └── pravesh.py        # Input/Output module
├── examples/                 # Example programs
│   ├── hello.mr
│   ├── fibonacci.mr
│   └── loops.mr
└── README.md                 # This file
```

## Error Handling

The interpreter provides error messages in both Marathi and English:
- Syntax errors show line and column information
- Runtime errors provide descriptive messages
- Unicode encoding issues are handled automatically

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## Troubleshooting

### Unicode Issues on Windows
If you encounter Unicode display issues:
1. Use `run_marathi.py` instead of `main.py`
2. Ensure your console supports UTF-8
3. The IDE handles Unicode automatically

### Common Issues
- **File not found**: Ensure the file path is correct and the file exists
- **Syntax errors**: Check for proper Marathi keywords and syntax
- **Runtime errors**: Verify variable declarations and function calls

## Future Enhancements

- VS Code extension for syntax highlighting
- More comprehensive standard library
- Package management system
- Advanced debugging features
- Web-based IDE
- Mobile app support

## License

This project is open source and available under the MIT License.

## Credits

Created to promote programming in regional languages and make coding accessible to Marathi speakers.

---

**मराठी भाषेतील प्रोग्रामिंग शिका आणि तंत्रज्ञानात योगदान द्या!**  
*Learn programming in Marathi and contribute to technology!*
