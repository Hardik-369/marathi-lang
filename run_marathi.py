#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper script for running Marathi code with proper Unicode support
"""

import sys
import os
import codecs

# Fix Unicode encoding issues on Windows
if sys.platform == 'win32':
    # Set console to UTF-8 mode
    try:
        # Change console code page to UTF-8
        os.system('chcp 65001 > nul')
        # Reconfigure stdout and stderr
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)
    except:
        pass

# Import and run the main module
if __name__ == "__main__":
    # Add the current directory to path
    sys.path.insert(0, os.path.dirname(__file__))
    
    # Import and run main
    from main import main
    main()
