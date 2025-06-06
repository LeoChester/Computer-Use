#!/usr/bin/env python3
"""
GitHub Repository Structure Creator for Computer Use Agent
Creates a complete, drag-and-drop GitHub repository with all installers.
"""

import os
import shutil
from pathlib import Path
import json
import subprocess
import zipfile

class GitHubRepoCreator:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.repo_dir = self.project_dir / "computer-use-agent-repo"
        
    def create_repo_structure(self):
        """Create GitHub repository directory structure"""
        print("📁 Creating GitHub repository structure...")
        
        # Clean and create main repo directory
        if self.repo_dir.exists():
            shutil.rmtree(self.repo_dir)
        self.repo_dir.mkdir()
        
        # Create directory structure
        dirs = [
            "src",
            "installers/windows",
            "installers/linux", 
            "installers/usb-creator",
            "docs",
            "screenshots",
            "models",
            ".github/workflows"
        ]
        
        for dir_path in dirs:
            (self.repo_dir / dir_path).mkdir(parents=True, exist_ok=True)
            
        print("✅ Repository structure created")
        
    def copy_source_files(self):
        """Copy source code to src directory"""
        print("💻 Copying source files...")
        
        source_files = [
            "ai_computer_agent.py",
            "computer_agent.py",
            "setup_models.py",
            "model_config.json",
            "create_installer.py",
            "create_linux_package.py",
            "create_deb_manual.py"
        ]
        
        for file in source_files:
            if Path(file).exists():
                shutil.copy2(file, self.repo_dir / "src" / file)
                
        print("✅ Source files copied")
        
    def copy_installers(self):
        """Copy all installer files"""
        print("📦 Copying installer files...")
        
        # Windows installers
        windows_files = [
            "ComputerUseAgent_Installer.exe",
            "install_computer_agent.py"
        ]
        
        installer_files_dir = Path("installer_files")
        if installer_files_dir.exists():
            shutil.copy2(
                installer_files_dir / "ComputerUseAgent_Portable.zip",
                self.repo_dir / "installers/windows/ComputerUseAgent_Portable.zip"
            )
            
        for file in windows_files:
            if Path(file).exists():
                shutil.copy2(file, self.repo_dir / "installers/windows" / file)
                
        # Linux installers
        linux_files = [
            "computer-use-agent_1.0.0_amd64.deb",
        ]
        
        for file in linux_files:
            if Path(file).exists():
                shutil.copy2(file, self.repo_dir / "installers/linux" / file)
                
        # Linux package files
        linux_package_dir = Path("linux_package")
        if linux_package_dir.exists():
            if (linux_package_dir / "computer-use-agent_1.0.0_linux.tar.gz").exists():
                shutil.copy2(
                    linux_package_dir / "computer-use-agent_1.0.0_linux.tar.gz",
                    self.repo_dir / "installers/linux/computer-use-agent_1.0.0_linux.tar.gz"
                )
            if (linux_package_dir / "install_linux.sh").exists():
                shutil.copy2(
                    linux_package_dir / "install_linux.sh",
                    self.repo_dir / "installers/linux/install_linux.sh"
                )
                
        print("✅ Installer files copied")
        
    def create_readme(self):
        """Create comprehensive README.md"""
        print("📝 Creating README.md...")
        
        readme_content = """# Computer Use Agent 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)]()

**AI-Powered Computer Automation with Computer Vision**

A sophisticated computer use agent that can see your screen, understand GUI elements, and perform complex automation tasks using natural language commands.

![Computer Use Agent Demo](screenshots/demo.gif)

## 🎯 Features

- **👁️ Visual Screen Understanding** - Analyzes screenshots using BLIP-2 vision models
- **🎯 GUI Element Detection** - Automatically finds buttons, text fields, and interactive elements
- **💬 Natural Language Control** - Execute commands like "Open calculator and compute 25 * 37"
- **📸 Screenshot Analysis** - Provides detailed descriptions of screen content
- **🖱️ Precise Automation** - Mouse clicks and keyboard input with pixel-perfect accuracy
- **🔄 Multi-step Workflows** - Execute complex sequences of actions
- **⚠️ Error Handling** - Adapts and recovers when automation fails
- **📱 Cross-Platform** - Works on Windows and Linux systems

## 🚀 Quick Start

### Windows

1. **Download the installer:**
   ```
   📥 Download: installers/windows/ComputerUseAgent_Installer.exe
   ```

2. **Run the installer:**
   - Double-click `ComputerUseAgent_Installer.exe`
   - The installer will automatically:
     - Install Python 3.11 if needed
     - Install all dependencies
     - Download AI models
     - Create desktop shortcuts

3. **Start using:**
   - Launch from Start Menu or Desktop
   - Begin with simple commands like "Take a screenshot"

### Linux (Ubuntu/Mint/Debian)

1. **Download the package:**
   ```bash
   wget https://github.com/your-username/computer-use-agent/releases/latest/download/computer-use-agent_1.0.0_amd64.deb
   ```

2. **Install:**
   ```bash
   sudo dpkg -i computer-use-agent_1.0.0_amd64.deb
   sudo apt-get install -f  # Fix any dependency issues
   ```

3. **Launch:**
   ```bash
   computer-use-agent
   # Or from Applications menu: Utilities → Computer Use Agent
   ```

## 📎 Installation Options

| Platform | Method | File | Size | Description |
|----------|--------|------|------|-------------|
| Windows | **EXE Installer** | `ComputerUseAgent_Installer.exe` | 8.5MB | Single-click install |
| Windows | Portable ZIP | `ComputerUseAgent_Portable.zip` | 13KB | Extract and run |
| Windows | Python Script | `install_computer_agent.py` | 7KB | For Python users |
| Linux | **Debian Package** | `computer-use-agent_1.0.0_amd64.deb` | 13KB | Recommended |
| Linux | Tarball | `computer-use-agent_1.0.0_linux.tar.gz` | 13KB | Manual install |
| Linux | Shell Script | `install_linux.sh` | 1KB | Root installer |

## 💻 Development

### Prerequisites
- Python 3.8+
- 4GB RAM minimum
- 2GB disk space
- Internet connection (for model downloads)

### Installation from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/computer-use-agent.git
   cd computer-use-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download AI models:**
   ```bash
   python src/setup_models.py
   ```

4. **Run the agent:**
   ```bash
   python src/ai_computer_agent.py
   ```

### Building Installers

**Windows:**
```bash
python src/create_installer.py
```

**Linux:**
```bash
python src/create_linux_package.py
```

## 🧪 Usage Examples

```python
# Natural language commands
agent.execute("Take a screenshot and describe what you see")
agent.execute("Find the calculator app and open it")
agent.execute("Click on the search box and type 'hello world'")
agent.execute("Find all PDF files on my desktop")
agent.execute("Open notepad and write a grocery list")
agent.execute("Resize the current window to half screen")
```

## 🔧 Technical Details

### AI Models
- **BLIP-2**: Image captioning and visual question answering
- **Vision Transformer**: GUI element detection
- **Local Processing**: All inference runs locally for privacy

### Dependencies
- PyTorch 2.0+ (CPU optimized)
- Transformers 4.25+
- OpenCV 4.5+ (computer vision)
- PyAutoGUI (GUI automation)
- Pynput (advanced input control)

### Architecture
```
┌───────────────────┐
│   User Interface    │
├───────────────────┤
│ Command Processor  │
├───────────────────┤
│  Vision Models     │
├───────────────────┤
│ Action Executor   │
├───────────────────┤
│ System Interface  │
└───────────────────┘
```

## 📷 Screenshots

| Main Interface | Settings Panel | Action Log |
|:-------------:|:-------------:|:----------:|
| ![Main](screenshots/main.png) | ![Settings](screenshots/settings.png) | ![Log](screenshots/log.png) |

## 📄 Documentation

- [Installation Guide](docs/installation.md)
- [User Manual](docs/user-guide.md)
- [API Reference](docs/api.md)
- [Development Guide](docs/development.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🎉 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚑 Support

- 🐛 [Bug Reports](https://github.com/your-username/computer-use-agent/issues)
- 💬 [Discussions](https://github.com/your-username/computer-use-agent/discussions)
- 📧 [Email Support](mailto:support@computeruse.ai)

## 🎆 Roadmap

- [ ] Web browser automation
- [ ] Mobile device control
- [ ] Voice command interface
- [ ] Multi-monitor support
- [ ] Cloud model options
- [ ] Plugin system

---

**Made with ❤️ by the Computer Use Agent Team**
"""
        
        with open(self.repo_dir / "README.md", "w", encoding='utf-8') as f:
            f.write(readme_content)
            
        print("✅ README.md created")
        
    def create_requirements_txt(self):
        """Create requirements.txt file"""
        print("📝 Creating requirements.txt...")
        
        requirements = """torch>=2.0.0
torchvision>=0.15.0
transformers>=4.25.0
acceleerate>=0.20.0
numpy>=1.21.0
pillow>=8.3.0
opencv-python>=4.5.0
pyautogui>=0.9.54
pynput>=1.7.6
screeninfo>=0.8
psutil>=5.8.0
requests>=2.25.0
"""
        
        with open(self.repo_dir / "requirements.txt", "w") as f:
            f.write(requirements)
            
        print("✅ requirements.txt created")
        
    def create_license(self):
        """Create MIT License file"""
        print("📜 Creating LICENSE...")
        
        license_content = """MIT License

Copyright (c) 2025 Computer Use Agent Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        
        with open(self.repo_dir / "LICENSE", "w") as f:
            f.write(license_content)
            
        print("✅ LICENSE created")
        
    def create_gitignore(self):
        """Create .gitignore file"""
        print("🚙 Creating .gitignore...")
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Models and cache
models/cache/
*.bin
*.safetensors

# User data
config/user_*
logs/
screenshots/temp/

# Build artifacts
build/
dist/
*.exe
*.deb
*.tar.gz
*.zip

# Secrets
.env
*.key
*.pem
"""
        
        with open(self.repo_dir / ".gitignore", "w") as f:
            f.write(gitignore_content)
            
        print("✅ .gitignore created")
        
    def create_github_workflows(self):
        """Create GitHub Actions workflows"""
        print("🔄 Creating GitHub workflows...")
        
        # CI workflow
        ci_workflow = """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v
        
    - name: Test model setup
      run: |
        python src/setup_models.py --test-only
"""
        
        with open(self.repo_dir / ".github/workflows/ci.yml", "w") as f:
            f.write(ci_workflow)
            
        # Release workflow
        release_workflow = """name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build Windows installer
      if: matrix.os == 'windows-latest'
      run: |
        python src/create_installer.py
    
    - name: Build Linux package
      if: matrix.os == 'ubuntu-latest'
      run: |
        sudo apt-get update
        sudo apt-get install -y dpkg-dev
        python src/create_linux_package.py
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: installers-${{ matrix.os }}
        path: |
          *.exe
          *.deb
          *.zip
          *.tar.gz
"""
        
        with open(self.repo_dir / ".github/workflows/release.yml", "w") as f:
            f.write(release_workflow)
            
        print("✅ GitHub workflows created")
        
    def create_documentation(self):
        """Create documentation files"""
        print("📚 Creating documentation...")
        
        # Installation guide
        install_guide = """# Installation Guide

## System Requirements

### Windows
- Windows 10 or later
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Internet connection for initial setup

### Linux
- Ubuntu 20.04+ / Linux Mint 20+ / Debian 11+
- X11 display server
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Internet connection for initial setup

## Windows Installation

### Option 1: EXE Installer (Recommended)
1. Download `ComputerUseAgent_Installer.exe`
2. Right-click and "Run as administrator"
3. Follow the installation wizard
4. Wait for AI models to download
5. Launch from Start Menu

### Option 2: Portable Version
1. Download `ComputerUseAgent_Portable.zip`
2. Extract to desired location
3. Run `INSTALL.bat`
4. Follow on-screen instructions

## Linux Installation

### Option 1: Debian Package (Recommended)
```bash
# Download the package
wget https://github.com/your-username/computer-use-agent/releases/latest/download/computer-use-agent_1.0.0_amd64.deb

# Install
sudo dpkg -i computer-use-agent_1.0.0_amd64.deb
sudo apt-get install -f

# Launch
computer-use-agent
```

### Option 2: Manual Installation
```bash
# Download and extract
wget https://github.com/your-username/computer-use-agent/releases/latest/download/computer-use-agent_1.0.0_linux.tar.gz
tar -xzf computer-use-agent_1.0.0_linux.tar.gz
cd computer-use-agent

# Install
sudo bash install_linux.sh
```

## Troubleshooting

### Windows
- **Python not found**: Installer will download Python automatically
- **Permission denied**: Run as administrator
- **Antivirus warning**: Add exception for installation directory

### Linux
- **Dependencies missing**: Run `sudo apt-get install -f`
- **X11 not available**: Ensure you're running a desktop environment
- **Permission denied**: Use `sudo` for installation commands
"""
        
        with open(self.repo_dir / "docs/installation.md", "w", encoding='utf-8') as f:
            f.write(install_guide)
            
        # User guide
        user_guide = """# User Guide

## Getting Started

### First Launch
1. Start Computer Use Agent
2. Wait for AI models to load (first time only)
3. The interface will show "Ready" when initialization is complete

### Basic Commands
- "Take a screenshot"
- "Describe what you see"
- "Find the calculator"
- "Click on [element]"
- "Type 'hello world'"

### Advanced Features
- Multi-step workflows
- GUI element detection
- Error recovery
- Screen understanding

## Command Examples

### Screenshot and Analysis
```
"Take a screenshot and describe what you see"
"What applications are currently open?"
"Find all buttons on the screen"
```

### Application Control
```
"Open calculator"
"Find and click the Settings button"
"Switch to the next window"
```

### Text Input
```
"Type 'Hello, world!' in the text field"
"Clear the current text and type [message]"
"Press Enter"
```

### File Operations
```
"Find all PDF files on the desktop"
"Open the file browser"
"Navigate to the Documents folder"
```

## Tips and Best Practices

1. **Be specific**: "Click the blue Save button" vs "Click Save"
2. **Wait for completion**: Let one command finish before the next
3. **Use natural language**: The AI understands conversational commands
4. **Check results**: Review what happened before continuing

## Limitations

- Works best with standard GUI applications
- May struggle with custom/non-standard interfaces
- Requires clear visual elements
- Performance depends on screen resolution
"""
        
        with open(self.repo_dir / "docs/user-guide.md", "w", encoding='utf-8') as f:
            f.write(user_guide)
            
        print("✅ Documentation created")
        
    def create_placeholder_screenshots(self):
        """Create placeholder screenshot files"""
        print("📷 Creating placeholder screenshots...")
        
        # Create simple placeholder images
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create main interface screenshot
            img = Image.new('RGB', (800, 600), color='#f0f0f0')
            draw = ImageDraw.Draw(img)
            draw.rectangle([50, 50, 750, 550], outline='#333', width=2)
            draw.text((300, 280), "Computer Use Agent", fill='#333')
            draw.text((320, 320), "Main Interface", fill='#666')
            img.save(self.repo_dir / "screenshots/main.png")
            
            # Create settings screenshot
            img2 = Image.new('RGB', (600, 400), color='#f8f8f8')
            draw2 = ImageDraw.Draw(img2)
            draw2.rectangle([20, 20, 580, 380], outline='#333', width=2)
            draw2.text((250, 180), "Settings Panel", fill='#333')
            img2.save(self.repo_dir / "screenshots/settings.png")
            
            # Create log screenshot
            img3 = Image.new('RGB', (700, 300), color='#ffffff')
            draw3 = ImageDraw.Draw(img3)
            draw3.rectangle([10, 10, 690, 290], outline='#333', width=2)
            draw3.text((300, 140), "Action Log", fill='#333')
            img3.save(self.repo_dir / "screenshots/log.png")
            
        except ImportError:
            # Create empty placeholder files
            placeholder_files = ["main.png", "settings.png", "log.png", "demo.gif"]
            for file in placeholder_files:
                (self.repo_dir / "screenshots" / file).touch()
                
        print("✅ Placeholder screenshots created")
        
    def create_usb_setup_tool(self):
        """Create USB setup tool"""
        print("💾 Creating USB setup tool...")
        
        usb_tool = """#!/usr/bin/env python3
# USB Setup Tool for Computer Use Agent
# Automatically copies all installers to a USB drive for easy distribution.
import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time

class USBSetupTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Computer Use Agent - USB Setup Tool")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.setup_ui()
        self.installers_dir = Path.cwd().parent
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Computer Use Agent USB Setup Tool", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="This tool will copy all Computer Use Agent installers to a USB drive\nfor easy distribution and offline installation.",
            justify=tk.CENTER
        )
        desc_label.pack(pady=(0, 20))
        
        # USB drive selection
        drive_frame = ttk.LabelFrame(main_frame, text="USB Drive Selection", padding="10")
        drive_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.drive_var = tk.StringVar()
        self.drive_combo = ttk.Combobox(
            drive_frame, 
            textvariable=self.drive_var,
            state="readonly",
            width=50
        )
        self.drive_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        refresh_btn = ttk.Button(
            drive_frame,
            text="Refresh",
            command=self.refresh_drives
        )
        refresh_btn.pack(side=tk.LEFT)
        
        # File list
        files_frame = ttk.LabelFrame(main_frame, text="Files to Copy", padding="10")
        files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create treeview for file list
        columns = ("File", "Platform", "Size", "Status")
        self.tree = ttk.Treeview(files_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "File":
                self.tree.column(col, width=250)
            elif col == "Platform":
                self.tree.column(col, width=80)
            elif col == "Size":
                self.tree.column(col, width=80)
            else:
                self.tree.column(col, width=100)
                
        scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(main_frame, text="Ready to copy files")
        self.status_label.pack()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.scan_btn = ttk.Button(
            button_frame,
            text="Scan for Installers",
            command=self.scan_installers
        )
        self.scan_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.copy_btn = ttk.Button(
            button_frame,
            text="Copy to USB",
            command=self.start_copy,
            state="disabled"
        )
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.exit_btn = ttk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit
        )
        self.exit_btn.pack(side=tk.RIGHT)
        
    def refresh_drives(self):
        """Refresh the list of available drives"""
        drives = []
        
        # Windows
        if os.name == 'nt':
            import string
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    try:
                        # Check if it's a removable drive
                        import win32file
                        drive_type = win32file.GetDriveType(drive)
                        if drive_type == win32file.DRIVE_REMOVABLE:
                            drives.append(f"{letter}: (Removable)")
                    except:
                        # Fallback - just show all drives
                        if os.path.ismount(drive):
                            drives.append(f"{letter}: (Drive)")
        
        # Linux/Mac
        else:
            media_dirs = ["/media", "/mnt", "/Volumes"]
            for media_dir in media_dirs:
                if os.path.exists(media_dir):
                    for item in os.listdir(media_dir):
                        item_path = os.path.join(media_dir, item)
                        if os.path.ismount(item_path):
                            drives.append(f"{item_path} ({item})")
        
        self.drive_combo['values'] = drives
        if drives:
            self.drive_combo.current(0)
            
    def scan_installers(self):
        """Scan for installer files"""
        self.tree.delete(*self.tree.get_children())
        
        installer_files = [
            ("ComputerUseAgent_Installer.exe", "Windows", "installers/windows/"),
            ("ComputerUseAgent_Portable.zip", "Windows", "installers/windows/"),
            ("install_computer_agent.py", "Windows", "installers/windows/"),
            ("computer-use-agent_1.0.0_amd64.deb", "Linux", "installers/linux/"),
            ("computer-use-agent_1.0.0_linux.tar.gz", "Linux", "installers/linux/"),
            ("install_linux.sh", "Linux", "installers/linux/")
        ]
        
        found_files = []
        
        for filename, platform, subdir in installer_files:
            file_path = self.installers_dir / subdir / filename
            if file_path.exists():
                size = file_path.stat().st_size
                if size > 1024*1024:
                    size_str = f"{size/1024/1024:.1f} MB"
                elif size > 1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size} B"
                    
                self.tree.insert("", tk.END, values=(filename, platform, size_str, "Ready"))
                found_files.append((filename, file_path))
                
        if found_files:
            self.copy_btn.config(state="normal")
            self.status_label.config(text=f"Found {len(found_files)} installer files")
        else:
            self.status_label.config(text="No installer files found")
            
        self.found_files = found_files
        
    def start_copy(self):
        """Start copying files in a separate thread"""
        if not self.drive_var.get():
            messagebox.showerror("Error", "Please select a USB drive")
            return
            
        self.copy_btn.config(state="disabled")
        self.scan_btn.config(state="disabled")
        
        thread = threading.Thread(target=self.copy_files)
        thread.daemon = True
        thread.start()
        
    def copy_files(self):
        """Copy files to USB drive"""
        try:
            # Get drive path
            drive_selection = self.drive_var.get()
            if "(" in drive_selection:
                drive_path = drive_selection.split(" (")[0]
                if os.name == 'nt' and not drive_path.endswith("\\"):
                    drive_path += "\\"
            else:
                drive_path = drive_selection
                
            # Create destination directory
            dest_dir = Path(drive_path) / "ComputerUseAgent_Installers"
            dest_dir.mkdir(exist_ok=True)
            
            # Create subdirectories
            (dest_dir / "Windows").mkdir(exist_ok=True)
            (dest_dir / "Linux").mkdir(exist_ok=True)
            
            total_files = len(self.found_files)
            
            for i, (filename, file_path) in enumerate(self.found_files):
                # Update status
                self.status_label.config(text=f"Copying {filename}...")
                
                # Determine destination
                if "deb" in filename or "linux" in filename or filename.endswith(".sh"):
                    dest_path = dest_dir / "Linux" / filename
                else:
                    dest_path = dest_dir / "Windows" / filename
                    
                # Copy file
                shutil.copy2(file_path, dest_path)
                
                # Update progress
                progress = ((i + 1) / total_files) * 100
                self.progress_var.set(progress)
                
                # Update tree
                for item in self.tree.get_children():
                    if self.tree.item(item, "values")[0] == filename:
                        values = list(self.tree.item(item, "values"))
                        values[3] = "Copied"
                        self.tree.item(item, values=values)
                        break
                        
                self.root.update()
                
            # Create README on USB
            readme_content = '''Computer Use Agent Installers
===============================

This USB drive contains installers for Computer Use Agent,
an AI-powered computer automation tool with computer vision.

Windows Installation:
- Run ComputerUseAgent_Installer.exe for automatic setup
- Or extract ComputerUseAgent_Portable.zip for portable version

Linux Installation:
- Install the .deb package with: sudo dpkg -i [deb-filename]
- Or use the manual installer: sudo bash install_linux.sh

For more information, visit:
https://github.com/your-username/computer-use-agent
'''
            
            with open(dest_dir / "README.txt", "w") as f:
                f.write(readme_content)
                
            self.status_label.config(text="All files copied successfully!")
            messagebox.showinfo("Success", f"All installer files copied to {dest_dir}")
            
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")
            messagebox.showerror("Error", f"Failed to copy files: {e}")
            
        finally:
            self.copy_btn.config(state="normal")
            self.scan_btn.config(state="normal")
            self.progress_var.set(0)
            
    def run(self):
        """Run the application"""
        self.refresh_drives()
        self.scan_installers()
        self.root.mainloop()

if __name__ == "__main__":
    app = USBSetupTool()
    app.run()
"""
        
        with open(self.repo_dir / "installers/usb-creator/usb_setup_tool.py", "w", encoding='utf-8') as f:
            f.write(usb_tool)
            
        # Create batch file for easy Windows launch
        batch_content = """@echo off
echo Starting USB Setup Tool...
python usb_setup_tool.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error: Python not found or script failed.
    echo Please ensure Python 3.8+ is installed.
    pause
)
"""
        
        with open(self.repo_dir / "installers/usb-creator/USB_Setup_Tool.bat", "w") as f:
            f.write(batch_content)
            
        # Create Linux launcher
        linux_launcher = """#!/bin/bash
echo "Starting USB Setup Tool..."
python3 usb_setup_tool.py
"""
        
        usb_linux_path = self.repo_dir / "installers/usb-creator/usb_setup_tool.sh"
        with open(usb_linux_path, "w") as f:
            f.write(linux_launcher)
        usb_linux_path.chmod(0o755)
        
        print("✅ USB setup tool created")
        
    def create_repo(self):
        """Create the complete GitHub repository"""
        print("🚀 Creating GitHub Repository")
        print("=" * 40)
        
        self.create_repo_structure()
        self.copy_source_files()
        self.copy_installers()
        self.create_readme()
        self.create_requirements_txt()
        self.create_license()
        self.create_gitignore()
        self.create_github_workflows()
        self.create_documentation()
        self.create_placeholder_screenshots()
        self.create_usb_setup_tool()
        
        print("\n🎉 GitHub repository created successfully!")
        print(f"\n📁 Repository location: {self.repo_dir}")
        print("\n🚀 Next steps:")
        print("1. cd computer-use-agent-repo")
        print("2. git init")
        print("3. git add .")
        print("4. git commit -m 'Initial commit'")
        print("5. Create repo on GitHub and push:")
        print("   git remote add origin https://github.com/yourusername/computer-use-agent.git")
        print("   git push -u origin main")
        
if __name__ == "__main__":
    creator = GitHubRepoCreator()
    creator.create_repo()

