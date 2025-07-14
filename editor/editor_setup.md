# Editor Setup Guide for Marathi Programming Language

## Overview
This guide helps you set up your development environment for writing programs in Marathi programming language.

## VS Code Extension

### Installation
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "marathi-lang" (when published)
4. Install the extension

### Features
- **Syntax Highlighting**: Marathi keywords highlighted in vibrant colors
- **Code Completion**: IntelliSense for Marathi language constructs
- **Error Detection**: Real-time syntax error highlighting
- **File Association**: Automatic recognition of `.mr` files

### Marathi Keywords Supported
```marathi
चल          // variable declaration
फंक्शन      // function
परत         // return
जर          // if condition
नाहीतर      // else
लूप         // loop
छाप         // print
```

## Other Editor Support

### Vim/Neovim
Create a syntax file at `~/.vim/syntax/marathi.vim`:
```vim
syntax keyword marathiKeyword चल फंक्शन परत जर नाहीतर लूप छाप
highlight marathiKeyword ctermfg=blue guifg=blue
```

### Sublime Text
1. Create new syntax file: `Marathi.sublime-syntax`
2. Add Marathi keyword patterns
3. Save in User packages folder

### Atom
Install the `language-marathi` package from Atom package manager.

## File Structure
```
project/
├── मुख्य.mr          // main file
├── फंक्शन्स.mr       // functions
└── टेस्ट.mr          // tests
```

## Sample Code
```marathi
चल नाव = "विकास"
चल वय = 25

फंक्शन अभिवादन(नाव) {
    छाप("नमस्कार " + नाव)
}

अभिवादन(नाव)
```

## Configuration
Add to your editor settings:
```json
{
    "files.associations": {
        "*.mr": "marathi"
    },
    "editor.fontSize": 14,
    "editor.fontFamily": "Noto Sans Devanagari, monospace"
}
```

## Font Recommendations
- **Noto Sans Devanagari**: Best for Devanagari script
- **Mangal**: Windows system font
- **Shree Devanagari**: Traditional appearance

## Debugging Setup
1. Install Marathi language debugger extension
2. Set breakpoints in `.mr` files
3. Use F5 to start debugging
4. View variables in Marathi in debug console

## Build Integration
Configure build tasks in your editor:
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Build Marathi",
            "type": "shell",
            "command": "marathi-compiler",
            "args": ["${file}"]
        }
    ]
}
```

## Troubleshooting
- **Characters not displaying**: Install Devanagari font
- **Syntax not highlighting**: Check file extension is `.mr`
- **IntelliSense not working**: Restart editor after extension install

## Contributing
Help improve editor support by:
1. Reporting bugs in syntax highlighting
2. Suggesting new language features
3. Contributing to open-source extensions
4. Testing on different operating systems

---
*Happy coding in Marathi! 🎉*
