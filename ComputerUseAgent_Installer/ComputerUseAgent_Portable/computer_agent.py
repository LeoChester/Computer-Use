import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import os
import webbrowser
import time
from datetime import datetime
import json

class ComputerUseAgent:
    def __init__(self, root):
        self.root = root
        self.root.title("Computer Use Agent")
        self.root.geometry("800x600")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Computer Use Agent", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Command Input", padding="5")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        self.command_entry = ttk.Entry(input_frame, font=('Arial', 11))
        self.command_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.command_entry.bind('<Return>', self.execute_command)
        
        execute_btn = ttk.Button(input_frame, text="Execute", command=self.execute_command)
        execute_btn.grid(row=0, column=1)
        
        # Quick actions frame
        actions_frame = ttk.LabelFrame(main_frame, text="Quick Actions", padding="5")
        actions_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Quick action buttons
        ttk.Button(actions_frame, text="Open Calculator", command=self.open_calculator).grid(row=0, column=0, padx=2)
        ttk.Button(actions_frame, text="Open Notepad", command=self.open_notepad).grid(row=0, column=1, padx=2)
        ttk.Button(actions_frame, text="Open Browser", command=self.open_browser).grid(row=0, column=2, padx=2)
        ttk.Button(actions_frame, text="List Files", command=self.list_files).grid(row=0, column=3, padx=2)
        ttk.Button(actions_frame, text="System Info", command=self.system_info).grid(row=0, column=4, padx=2)
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="5")
        output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, font=('Consolas', 10))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Initialize
        self.log_message("Computer Use Agent initialized")
        self.log_message("Type commands or use quick actions to control your computer")
        self.log_message("-" * 50)
        
    def log_message(self, message):
        """Add a message to the output log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
        
    def execute_command(self, event=None):
        """Execute the command entered by the user"""
        command = self.command_entry.get().strip()
        if not command:
            return
            
        self.command_entry.delete(0, tk.END)
        self.status_var.set("Executing...")
        self.log_message(f"Executing: {command}")
        
        try:
            # Handle special commands
            if command.lower().startswith('open '):
                self.handle_open_command(command[5:])
            elif command.lower() == 'clear':
                self.output_text.delete(1.0, tk.END)
                self.log_message("Output cleared")
            elif command.lower() in ['exit', 'quit']:
                self.root.quit()
            else:
                # Execute as shell command
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.stdout:
                    self.log_message(f"Output:\n{result.stdout}")
                if result.stderr:
                    self.log_message(f"Error:\n{result.stderr}")
                if result.returncode != 0:
                    self.log_message(f"Command failed with exit code: {result.returncode}")
                    
        except Exception as e:
            self.log_message(f"Error executing command: {str(e)}")
            
        self.status_var.set("Ready")
        
    def handle_open_command(self, target):
        """Handle 'open' commands"""
        try:
            if target.lower() in ['calculator', 'calc']:
                self.open_calculator()
            elif target.lower() in ['notepad', 'text']:
                self.open_notepad()
            elif target.lower() in ['browser', 'web']:
                self.open_browser()
            elif os.path.exists(target):
                os.startfile(target)
                self.log_message(f"Opened: {target}")
            else:
                # Try to open as URL
                webbrowser.open(target)
                self.log_message(f"Opened URL: {target}")
        except Exception as e:
            self.log_message(f"Error opening {target}: {str(e)}")
            
    def open_calculator(self):
        """Open Windows Calculator"""
        try:
            subprocess.Popen(['calc.exe'])
            self.log_message("Opened Calculator")
        except Exception as e:
            self.log_message(f"Error opening Calculator: {str(e)}")
            
    def open_notepad(self):
        """Open Notepad"""
        try:
            subprocess.Popen(['notepad.exe'])
            self.log_message("Opened Notepad")
        except Exception as e:
            self.log_message(f"Error opening Notepad: {str(e)}")
            
    def open_browser(self):
        """Open default web browser"""
        try:
            webbrowser.open('https://www.google.com')
            self.log_message("Opened web browser")
        except Exception as e:
            self.log_message(f"Error opening browser: {str(e)}")
            
    def list_files(self):
        """List files in current directory"""
        try:
            result = subprocess.run(['dir'], shell=True, capture_output=True, text=True)
            self.log_message("Current directory contents:")
            self.log_message(result.stdout)
        except Exception as e:
            self.log_message(f"Error listing files: {str(e)}")
            
    def system_info(self):
        """Display system information"""
        try:
            result = subprocess.run(['systeminfo'], shell=True, capture_output=True, text=True)
            lines = result.stdout.split('\n')[:10]  # First 10 lines
            self.log_message("System Information (first 10 lines):")
            self.log_message('\n'.join(lines))
        except Exception as e:
            self.log_message(f"Error getting system info: {str(e)}")

def main():
    root = tk.Tk()
    app = ComputerUseAgent(root)
    root.mainloop()

if __name__ == "__main__":
    main()

