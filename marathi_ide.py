import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, Menu
import subprocess
import os
import sys
from pathlib import Path

class MarathiIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Marathi Language IDE - मराठी भाषा IDE")
        self.geometry("1000x700")
        self.configure(bg='#f0f0f0')
        
        # Create main frame
        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create menu
        self.create_menu()
        
        # Create toolbar
        self.create_toolbar(main_frame)
        
        # Create editor frame
        editor_frame = tk.Frame(main_frame, bg='#f0f0f0')
        editor_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 5))
        
        # Editor label
        editor_label = tk.Label(editor_frame, text="Code Editor:", bg='#f0f0f0', font=("Arial", 11, "bold"))
        editor_label.pack(anchor=tk.W)
        
        # Create editor with line numbers
        self.editor = scrolledtext.ScrolledText(
            editor_frame, 
            wrap=tk.NONE, 
            font=("Consolas", 11), 
            bg='white', 
            fg='black',
            insertbackground='black',
            selectbackground='#316AC5',
            height=20
        )
        self.editor.pack(fill=tk.BOTH, expand=True)
        
        # Add sample code
        sample_code = '''// मराठी भाषा उदाहरण
चल नाव = "राम"
मुद्रण("नमस्कार", नाव)

चल संख्या = ५
कार्य वर्ग(x) {
    परत x * x
}

मुद्रण("वर्ग:", वर्ग(संख्या))'''
        
        self.editor.insert(tk.END, sample_code)
        
        # Create output frame
        output_frame = tk.Frame(main_frame, bg='#f0f0f0')
        output_frame.pack(fill=tk.BOTH, expand=False, pady=(5, 0))
        
        # Output label
        output_label = tk.Label(output_frame, text="Output:", bg='#f0f0f0', font=("Arial", 11, "bold"))
        output_label.pack(anchor=tk.W)
        
        # Create output area
        self.output = scrolledtext.ScrolledText(
            output_frame, 
            wrap=tk.WORD, 
            background="#1e1e1e", 
            foreground="#ffffff",
            state='disabled', 
            height=10,
            font=("Consolas", 10)
        )
        self.output.pack(fill=tk.BOTH, expand=False)
        
        # Status bar
        self.status_bar = tk.Label(self, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg='#e0e0e0')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind keyboard shortcuts
        self.bind('<Control-r>', lambda e: self.run_code())
        self.bind('<F5>', lambda e: self.run_code())
        
    def create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        
        # Run menu
        run_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run Code", command=self.run_code, accelerator="F5")
        run_menu.add_command(label="Clear Output", command=self.clear_output)
        
        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.bind('<Control-n>', lambda e: self.new_file())
        self.bind('<Control-o>', lambda e: self.open_file())
        self.bind('<Control-s>', lambda e: self.save_file())
        
    def create_toolbar(self, parent):
        toolbar = tk.Frame(parent, bg='#e0e0e0', relief=tk.RAISED, bd=1)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        # Run button
        run_btn = tk.Button(
            toolbar, 
            text="▶ Run (F5)", 
            command=self.run_code, 
            bg='#4CAF50', 
            fg='white',
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=20
        )
        run_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Clear button
        clear_btn = tk.Button(
            toolbar, 
            text="Clear Output", 
            command=self.clear_output,
            bg='#f44336',
            fg='white',
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15
        )
        clear_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # New file button
        new_btn = tk.Button(
            toolbar,
            text="New",
            command=self.new_file,
            bg='#2196F3',
            fg='white',
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15
        )
        new_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Open file button
        open_btn = tk.Button(
            toolbar,
            text="Open",
            command=self.open_file,
            bg='#FF9800',
            fg='white',
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15
        )
        open_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Save file button
        save_btn = tk.Button(
            toolbar,
            text="Save",
            command=self.save_file,
            bg='#9C27B0',
            fg='white',
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15
        )
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
    def new_file(self):
        self.editor.delete("1.0", tk.END)
        self.clear_output()
        self.status_bar.config(text="New file created")
        
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Open Marathi File",
            filetypes=[("Marathi files", "*.mr"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", content)
                self.status_bar.config(text=f"Opened: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")
                
    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Marathi File",
            defaultextension=".mr",
            filetypes=[("Marathi files", "*.mr"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.editor.get("1.0", tk.END))
                self.status_bar.config(text=f"Saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
                
    def clear_output(self):
        self.output.configure(state='normal')
        self.output.delete("1.0", tk.END)
        self.output.configure(state='disabled')
        self.status_bar.config(text="Output cleared")
        
    def show_about(self):
        messagebox.showinfo(
            "About",
            "Marathi Language IDE\n\nA simple IDE for the Marathi programming language.\n\nFeatures:\n- Syntax highlighting support\n- Code execution\n- File operations\n\nKeyboard shortcuts:\n- F5 or Ctrl+R: Run code\n- Ctrl+N: New file\n- Ctrl+O: Open file\n- Ctrl+S: Save file"
        )
        
    def run_code(self):
        code = self.editor.get("1.0", tk.END).strip()
        
        if not code:
            messagebox.showwarning("Warning", "Please enter some code to run.")
            return
            
        self.status_bar.config(text="Running code...")
        self.update()
        
        try:
            # Save code to temporary file
            temp_file = "temp.mr"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(code)
            
            # Get the current directory
            current_dir = os.getcwd()
            
            # Run the code using the interpreter
            # Set environment variables for proper Unicode handling
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONLEGACYWINDOWSSTDIO'] = '1'
            
            result = subprocess.run(
                [sys.executable, "run_marathi.py", temp_file], 
                capture_output=True, 
                text=True, 
                cwd=current_dir,
                encoding='utf-8',
                env=env
            )
            
            # Display output
            self.output.configure(state='normal')
            self.output.delete("1.0", tk.END)
            
            if result.stdout:
                self.output.insert(tk.END, "Output:\n")
                self.output.insert(tk.END, result.stdout)
                self.output.insert(tk.END, "\n")
                
            if result.stderr:
                self.output.insert(tk.END, "Errors:\n")
                self.output.insert(tk.END, result.stderr)
                
            if not result.stdout and not result.stderr:
                self.output.insert(tk.END, "Code executed successfully (no output)")
                
            self.output.configure(state='disabled')
            self.status_bar.config(text="Code execution completed")
            
        except Exception as e:
            self.output.configure(state='normal')
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"Error running code: {str(e)}")
            self.output.configure(state='disabled')
            self.status_bar.config(text="Error occurred")
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass

if __name__ == "__main__":
    app = MarathiIDE()
    app.mainloop()

