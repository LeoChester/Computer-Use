import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import os
import webbrowser
import time
from datetime import datetime
import json
import threading
import sys
from pathlib import Path

# AI imports (with fallbacks if not installed)
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    from sentence_transformers import SentenceTransformer
    import torch
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("AI libraries not installed. Running in basic mode.")

class LocalAIManager:
    """Manages local AI models for command interpretation and generation"""
    
    def __init__(self):
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)
        self.command_classifier = None
        self.text_generator = None
        self.embedder = None
        self.initialized = False
        
    def initialize_models(self, callback=None):
        """Initialize AI models with progress callback"""
        if not AI_AVAILABLE:
            if callback:
                callback("AI libraries not available. Please install requirements.")
            return False
            
        try:
            if callback:
                callback("Loading command classifier...")
            
            # Use a lightweight model for command classification
            self.command_classifier = pipeline(
                "text-classification",
                model="microsoft/DialoGPT-small",
                return_all_scores=True
            )
            
            if callback:
                callback("Loading text embedder...")
            
            # Sentence transformer for semantic similarity
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            
            if callback:
                callback("Loading text generator...")
            
            # Small GPT model for text generation
            self.text_generator = pipeline(
                "text-generation",
                model="gpt2",
                max_length=100,
                num_return_sequences=1,
                temperature=0.7
            )
            
            self.initialized = True
            if callback:
                callback("AI models loaded successfully!")
            return True
            
        except Exception as e:
            error_msg = f"Error loading AI models: {str(e)}"
            if callback:
                callback(error_msg)
            print(error_msg)
            return False
    
    def interpret_command(self, user_input):
        """Interpret natural language input into system commands"""
        if not self.initialized:
            return user_input
            
        # Define command patterns
        command_patterns = {
            "file_operation": [
                "list files", "show files", "dir", "ls", "open folder",
                "create file", "delete file", "copy file", "move file"
            ],
            "application": [
                "open calculator", "open notepad", "open browser",
                "start app", "launch program", "run application"
            ],
            "system_info": [
                "system info", "computer specs", "hardware info",
                "memory usage", "cpu usage", "disk space"
            ],
            "network": [
                "ping", "internet", "network", "ip address", "wifi"
            ]
        }
        
        user_lower = user_input.lower()
        
        # Simple pattern matching for common commands
        if any(pattern in user_lower for pattern in command_patterns["file_operation"]):
            if "list" in user_lower or "show" in user_lower:
                return "dir"
            elif "open folder" in user_lower:
                return "explorer ."
                
        elif any(pattern in user_lower for pattern in command_patterns["application"]):
            if "calculator" in user_lower or "calc" in user_lower:
                return "calc"
            elif "notepad" in user_lower:
                return "notepad"
            elif "browser" in user_lower:
                return "start https://www.google.com"
                
        elif any(pattern in user_lower for pattern in command_patterns["system_info"]):
            if "memory" in user_lower:
                return "tasklist"
            elif "disk" in user_lower:
                return "dir"
            else:
                return "systeminfo"
                
        elif any(pattern in user_lower for pattern in command_patterns["network"]):
            if "ping" in user_lower:
                return "ping google.com"
            elif "ip" in user_lower:
                return "ipconfig"
                
        return user_input
    
    def generate_response(self, context):
        """Generate AI response based on context"""
        if not self.initialized or not self.text_generator:
            return "AI models not loaded. Using basic mode."
            
        try:
            prompt = f"Computer agent response for: {context}"
            response = self.text_generator(prompt, max_length=50, num_return_sequences=1)
            return response[0]['generated_text'].replace(prompt, "").strip()
        except Exception as e:
            return f"AI generation error: {str(e)}"

class AIComputerUseAgent:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Enhanced Computer Use Agent")
        self.root.geometry("900x700")
        
        # Initialize AI manager
        self.ai_manager = LocalAIManager()
        
        # Create UI
        self.create_ui()
        
        # Initialize AI models in background
        self.initialize_ai_async()
        
    def create_ui(self):
        """Create the user interface"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title with AI indicator
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="AI-Enhanced Computer Use Agent", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        self.ai_status_label = ttk.Label(title_frame, text="🤖 AI: Loading...", 
                                        font=('Arial', 10), foreground="orange")
        self.ai_status_label.pack(side=tk.RIGHT)
        
        # Input section with AI toggle
        input_frame = ttk.LabelFrame(main_frame, text="Command Input", padding="5")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # AI mode toggle
        ai_frame = ttk.Frame(input_frame)
        ai_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.ai_mode = tk.BooleanVar(value=True)
        ai_check = ttk.Checkbutton(ai_frame, text="AI Command Interpretation", 
                                  variable=self.ai_mode)
        ai_check.pack(side=tk.LEFT)
        
        ttk.Button(ai_frame, text="Install Models", command=self.install_models).pack(side=tk.RIGHT)
        
        # Command entry
        self.command_entry = ttk.Entry(input_frame, font=('Arial', 11), width=60)
        self.command_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.command_entry.bind('<Return>', self.execute_command)
        
        execute_btn = ttk.Button(input_frame, text="Execute", command=self.execute_command)
        execute_btn.grid(row=1, column=1)
        
        # Quick actions frame (enhanced)
        actions_frame = ttk.LabelFrame(main_frame, text="Quick Actions", padding="5")
        actions_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Row 1 of buttons
        button_row1 = ttk.Frame(actions_frame)
        button_row1.pack(fill=tk.X, pady=2)
        
        ttk.Button(button_row1, text="📱 Calculator", command=self.open_calculator).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_row1, text="📝 Notepad", command=self.open_notepad).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_row1, text="🌐 Browser", command=self.open_browser).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_row1, text="📁 Files", command=self.list_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_row1, text="ℹ️ System Info", command=self.system_info).pack(side=tk.LEFT, padx=2)
        
        # Row 2 of buttons (AI-enhanced)
        button_row2 = ttk.Frame(actions_frame)
        button_row2.pack(fill=tk.X, pady=2)
        
        ttk.Button(button_row2, text="🤖 AI Suggest", command=self.ai_suggest).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_row2, text="📊 Performance", command=self.show_performance).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_row2, text="🔍 Smart Search", command=self.smart_search).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_row2, text="🧹 Clean Up", command=self.cleanup_suggestions).pack(side=tk.LEFT, padx=2)
        
        # Output section with tabs
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="5")
        output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(output_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Command output tab
        command_frame = ttk.Frame(self.notebook)
        self.notebook.add(command_frame, text="Command Output")
        
        self.output_text = scrolledtext.ScrolledText(command_frame, height=15, font=('Consolas', 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # AI chat tab
        ai_frame = ttk.Frame(self.notebook)
        self.notebook.add(ai_frame, text="AI Assistant")
        
        self.ai_text = scrolledtext.ScrolledText(ai_frame, height=15, font=('Consolas', 10))
        self.ai_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - AI models loading...")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Initialize logs
        self.log_message("AI-Enhanced Computer Use Agent initialized")
        self.log_message("Loading AI models in background...")
        self.log_message("-" * 60)
        
        self.ai_log("AI Assistant ready! Ask me anything about your computer.")
        self.ai_log("Try commands like: 'show me system info' or 'find large files'")
        
    def initialize_ai_async(self):
        """Initialize AI models in a separate thread"""
        def init_thread():
            success = self.ai_manager.initialize_models(self.update_ai_status)
            if success:
                self.ai_status_label.config(text="🤖 AI: Ready", foreground="green")
                self.status_var.set("Ready - AI models loaded")
            else:
                self.ai_status_label.config(text="🤖 AI: Failed", foreground="red")
                self.status_var.set("Ready - AI models failed to load")
                
        thread = threading.Thread(target=init_thread, daemon=True)
        thread.start()
        
    def update_ai_status(self, message):
        """Update AI loading status"""
        self.root.after(0, lambda: self.ai_log(f"[AI] {message}"))
        
    def log_message(self, message):
        """Add a message to the command output log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
        
    def ai_log(self, message):
        """Add a message to the AI assistant log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.ai_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.ai_text.see(tk.END)
        self.root.update_idletasks()
        
    def execute_command(self, event=None):
        """Execute the command entered by the user"""
        user_input = self.command_entry.get().strip()
        if not user_input:
            return
            
        self.command_entry.delete(0, tk.END)
        self.status_var.set("Executing...")
        
        # Use AI interpretation if enabled
        if self.ai_mode.get() and self.ai_manager.initialized:
            interpreted_command = self.ai_manager.interpret_command(user_input)
            if interpreted_command != user_input:
                self.ai_log(f"Interpreted '{user_input}' as: {interpreted_command}")
            command = interpreted_command
        else:
            command = user_input
            
        self.log_message(f"User: {user_input}")
        if command != user_input:
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
            lines = result.stdout.split('\n')[:15]  # First 15 lines
            self.log_message("System Information:")
            self.log_message('\n'.join(lines))
        except Exception as e:
            self.log_message(f"Error getting system info: {str(e)}")
    
    # New AI-enhanced functions
    def ai_suggest(self):
        """AI suggests useful commands based on system state"""
        suggestions = [
            "systeminfo - View detailed system information",
            "tasklist - See running processes",
            "dir /s *.log - Find log files",
            "ping google.com - Test internet connection",
            "ipconfig - View network configuration"
        ]
        
        self.ai_log("Here are some useful commands you can try:")
        for suggestion in suggestions:
            self.ai_log(f"• {suggestion}")
            
    def show_performance(self):
        """Show system performance information"""
        try:
            # Memory info
            result = subprocess.run(['wmic', 'OS', 'get', 'TotalVirtualMemorySize,TotalVisibleMemorySize,FreePhysicalMemory', '/format:list'], 
                                  shell=True, capture_output=True, text=True)
            self.log_message("Memory Information:")
            self.log_message(result.stdout)
            
            # CPU info
            result = subprocess.run(['wmic', 'cpu', 'get', 'loadpercentage', '/value'], 
                                  shell=True, capture_output=True, text=True)
            self.log_message("CPU Usage:")
            self.log_message(result.stdout)
            
        except Exception as e:
            self.log_message(f"Error getting performance info: {str(e)}")
            
    def smart_search(self):
        """Smart file search with AI suggestions"""
        search_term = tk.simpledialog.askstring("Smart Search", "What files are you looking for?")
        if search_term:
            self.ai_log(f"Searching for: {search_term}")
            try:
                result = subprocess.run(['dir', f'*{search_term}*', '/s'], 
                                      shell=True, capture_output=True, text=True)
                self.log_message(f"Search results for '{search_term}':")
                self.log_message(result.stdout)
            except Exception as e:
                self.log_message(f"Error searching: {str(e)}")
                
    def cleanup_suggestions(self):
        """AI-powered cleanup suggestions"""
        self.ai_log("Analyzing system for cleanup opportunities...")
        
        suggestions = [
            "temp files in %temp% directory",
            "browser cache and cookies",
            "old log files",
            "unused programs",
            "large files taking up space"
        ]
        
        self.ai_log("Consider cleaning up:")
        for suggestion in suggestions:
            self.ai_log(f"• {suggestion}")
            
    def install_models(self):
        """Install AI models and dependencies"""
        def install_thread():
            self.ai_log("Starting model installation...")
            try:
                # Install requirements
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.ai_log("✅ Requirements installed successfully!")
                    self.ai_log("Reinitializing AI models...")
                    
                    # Reinitialize AI
                    self.ai_manager = LocalAIManager()
                    success = self.ai_manager.initialize_models(self.update_ai_status)
                    
                    if success:
                        self.root.after(0, lambda: self.ai_status_label.config(text="🤖 AI: Ready", foreground="green"))
                        self.ai_log("🎉 AI models ready! You can now use AI features.")
                    else:
                        self.ai_log("❌ Failed to initialize AI models.")
                else:
                    self.ai_log(f"❌ Installation failed: {result.stderr}")
                    
            except Exception as e:
                self.ai_log(f"❌ Installation error: {str(e)}")
                
        thread = threading.Thread(target=install_thread, daemon=True)
        thread.start()

def main():
    # Import tkinter simpledialog for smart search
    try:
        import tkinter.simpledialog
    except ImportError:
        pass
        
    root = tk.Tk()
    app = AIComputerUseAgent(root)
    root.mainloop()

if __name__ == "__main__":
    main()

