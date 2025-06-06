#!/usr/bin/env python3
"""
Computer Use Agent - Linux .deb Package Creator
This script creates a Debian package for Linux Mint and other Debian-based systems.
"""

import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path
import json
import tempfile
import stat

class LinuxPackageCreator:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.package_dir = self.project_dir / "linux_package"
        self.debian_dir = self.package_dir / "computer-use-agent_1.0.0_amd64"
        self.app_name = "computer-use-agent"
        self.version = "1.0.0"
        
    def clean_build_dirs(self):
        """Clean previous build directories"""
        print("🧹 Cleaning Linux build directories...")
        if self.package_dir.exists():
            shutil.rmtree(self.package_dir)
        
        # Create fresh directories
        self.package_dir.mkdir(exist_ok=True)
        self.debian_dir.mkdir(exist_ok=True)
        
    def create_debian_structure(self):
        """Create standard Debian package structure"""
        print("📁 Creating Debian package structure...")
        
        # Standard Debian directories
        dirs = [
            "DEBIAN",
            "usr/bin",
            "usr/share/applications",
            "usr/share/computer-use-agent",
            "usr/share/computer-use-agent/models",
            "usr/share/icons/hicolor/64x64/apps",
            "usr/share/doc/computer-use-agent",
            "etc/computer-use-agent"
        ]
        
        for dir_path in dirs:
            (self.debian_dir / dir_path).mkdir(parents=True, exist_ok=True)
            
        print("✅ Debian directory structure created")
        
    def create_control_file(self):
        """Create the DEBIAN/control file"""
        print("📝 Creating control file...")
        
        control_content = f"""Package: {self.app_name}
Version: {self.version}
Section: utils
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.8), python3-pip, python3-venv, python3-tk, x11-utils, xdotool, scrot
Maintainer: Computer Use Agent Team <admin@computeruse.ai>
Description: AI-powered computer use agent with vision capabilities
 An intelligent computer automation agent that can see your screen,
 understand GUI elements, and perform complex tasks using natural language.
 Features include:
  - Visual screen understanding and analysis
  - GUI element detection and interaction
  - Natural language to computer actions
  - Screenshot analysis and description
  - Mouse and keyboard automation
  - Multi-step task execution
  - Error detection and correction
Homepage: https://github.com/computeruse/agent
"""
        
        with open(self.debian_dir / "DEBIAN/control", "w") as f:
            f.write(control_content)
            
        print("✅ Control file created")
        
    def create_postinst_script(self):
        """Create post-installation script"""
        print("📝 Creating post-install script...")
        
        postinst_content = """#!/bin/bash
set -e

echo "Setting up Computer Use Agent..."

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv /usr/share/computer-use-agent/venv

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source /usr/share/computer-use-agent/venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Install dependencies with specific versions for compatibility
echo "Installing PyTorch..."
pip install torch==2.0.1 torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cpu

echo "Installing computer vision dependencies..."
pip install transformers==4.30.2
pip install accelerate==0.20.3
pip install numpy==1.24.3
pip install pillow==10.0.0
pip install opencv-python==4.8.0.74
pip install pyautogui==0.9.54
pip install pynput==1.7.6
pip install screeninfo==0.8.1
pip install psutil==5.9.5
pip install requests==2.31.0

# Download AI models
echo "Downloading AI models (this may take a few minutes)..."
cd /usr/share/computer-use-agent
python3 setup_models_linux.py

# Set permissions
chmod +x /usr/bin/computer-use-agent
chmod +x /usr/share/computer-use-agent/launch.sh

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications
fi

echo "Computer Use Agent installation completed successfully!"
echo "You can start it from the applications menu or run 'computer-use-agent' in terminal."

exit 0
"""
        
        postinst_path = self.debian_dir / "DEBIAN/postinst"
        with open(postinst_path, "w") as f:
            f.write(postinst_content)
            
        # Make executable
        postinst_path.chmod(0o755)
        print("✅ Post-install script created")
        
    def create_prerm_script(self):
        """Create pre-removal script"""
        print("📝 Creating pre-removal script...")
        
        prerm_content = """#!/bin/bash
set -e

echo "Removing Computer Use Agent..."

# Stop any running instances
pkill -f "computer-use-agent" || true

# Remove virtual environment
if [ -d "/usr/share/computer-use-agent/venv" ]; then
    rm -rf /usr/share/computer-use-agent/venv
fi

# Remove downloaded models
if [ -d "/usr/share/computer-use-agent/models" ]; then
    rm -rf /usr/share/computer-use-agent/models
fi

exit 0
"""
        
        prerm_path = self.debian_dir / "DEBIAN/prerm"
        with open(prerm_path, "w") as f:
            f.write(prerm_content)
            
        prerm_path.chmod(0o755)
        print("✅ Pre-removal script created")
        
    def create_desktop_file(self):
        """Create .desktop file for application menu"""
        print("📝 Creating desktop entry...")
        
        desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=Computer Use Agent
Comment=AI-powered computer automation with vision
Exec=computer-use-agent
Icon=computer-use-agent
Terminal=false
StartupNotify=true
Categories=Utility;System;Accessibility;
Keywords=automation;ai;computer;vision;gui;assistant;
MimeType=
"""
        
        with open(self.debian_dir / "usr/share/applications/computer-use-agent.desktop", "w") as f:
            f.write(desktop_content)
            
        print("✅ Desktop entry created")
        
    def create_icon(self):
        """Create application icon"""
        print("🎨 Creating application icon...")
        
        # Create a simple SVG icon (since we don't have an existing one)
        icon_svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" rx="8" fill="#2563eb"/>
  <circle cx="20" cy="20" r="6" fill="#ffffff"/>
  <circle cx="44" cy="20" r="6" fill="#ffffff"/>
  <rect x="16" y="40" width="32" height="4" rx="2" fill="#ffffff"/>
  <rect x="20" y="48" width="24" height="3" rx="1.5" fill="#ffffff"/>
</svg>
"""
        
        icon_path = self.debian_dir / "usr/share/icons/hicolor/64x64/apps/computer-use-agent.svg"
        with open(icon_path, "w") as f:
            f.write(icon_svg)
            
        print("✅ Application icon created")
        
    def create_launcher_script(self):
        """Create the main launcher script"""
        print("📝 Creating launcher script...")
        
        launcher_content = """#!/bin/bash
# Computer Use Agent Launcher for Linux

APP_DIR="/usr/share/computer-use-agent"
VENV_DIR="$APP_DIR/venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Computer Use Agent is not properly installed."
    echo "Please reinstall the package."
    exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Change to application directory
cd "$APP_DIR"

# Set display for GUI applications
export DISPLAY=${DISPLAY:-:0}

# Start the application
python3 ai_computer_agent_linux.py "$@"
"""
        
        # Main launcher in /usr/bin
        launcher_path = self.debian_dir / "usr/bin/computer-use-agent"
        with open(launcher_path, "w") as f:
            f.write(launcher_content)
        launcher_path.chmod(0o755)
        
        # Secondary launcher script
        launch_sh_path = self.debian_dir / "usr/share/computer-use-agent/launch.sh"
        with open(launch_sh_path, "w") as f:
            f.write(launcher_content)
        launch_sh_path.chmod(0o755)
        
        print("✅ Launcher scripts created")
        
    def create_linux_setup_models(self):
        """Create Linux-specific setup_models.py"""
        print("📝 Creating Linux model setup script...")
        
        setup_content = """#!/usr/bin/env python3
# Computer Use Agent - Linux Model Setup
# Downloads and configures AI models for Linux systems.
import os
import sys
import subprocess
from pathlib import Path
import json

def check_python_version():
    # Check if Python version is compatible
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def download_models():
    # Download and cache vision-language models for computer use
    print("🤖 Preparing computer vision models for GUI control...")
    
    try:
        # Import after installation
        from transformers import BlipProcessor, BlipForConditionalGeneration
        import torch
        from PIL import Image
        import numpy as np
        
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        print("Downloading BLIP-2 model for visual question answering...")
        # BLIP-2 is good for understanding screenshots and answering questions about them
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        model.to(device)
        print("✅ BLIP-2 vision model ready")
        
        # Test the models with a dummy image
        print("🧪 Testing vision models...")
        
        # Create a test image (screenshot-like)
        test_image = Image.new('RGB', (800, 600), color='white')
        
        # Test BLIP-2
        inputs = processor(test_image, return_tensors="pt").to(device)
        out = model.generate(**inputs, max_length=50)
        caption = processor.decode(out[0], skip_special_tokens=True)
        print(f"✅ Vision model test passed: {caption}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        return False
    except Exception as e:
        print(f"❌ Error downloading models: {e}")
        return False

def create_model_config():
    # Create configuration file for vision models
    import torch
    
    config = {
        "models": {
            "vision_language": {
                "name": "Salesforce/blip-image-captioning-base",
                "type": "blip",
                "local_path": "models/vision_language/blip",
                "capabilities": ["image_captioning", "visual_qa", "screen_understanding"]
            }
        },
        "settings": {
            "device": "cuda" if torch.cuda.is_available() else "cpu",
            "max_length": 512,
            "temperature": 0.7,
            "cache_dir": "models/cache",
            "screenshot_interval": 1.0,
            "gui_detection_threshold": 0.7
        },
        "computer_use": {
            "screen_resolution": "auto",
            "mouse_precision": "high",
            "keyboard_delay": 0.1,
            "action_delay": 0.5
        }
    }
    
    with open("model_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Model configuration saved")

def main():
    # Main setup function
    print("🚀 Computer Use Agent - Linux Model Setup")
    print("==========================================\n")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    (models_dir / "vision_language").mkdir(exist_ok=True)
    (models_dir / "cache").mkdir(exist_ok=True)
    
    # Download models
    models_ready = download_models()
    
    if models_ready:
        create_model_config()
        print("\n🎉 Linux model setup complete!")
        return True
    else:
        print("\n❌ Model setup failed")
        return False

if __name__ == "__main__":
    main()
"""
        
        with open(self.debian_dir / "usr/share/computer-use-agent/setup_models_linux.py", "w", encoding='utf-8') as f:
            f.write(setup_content)
            
        print("✅ Linux model setup script created")
        
    def create_linux_main_app(self):
        """Create Linux-adapted main application"""
        print("📝 Creating Linux main application...")
        
        # Read the original Windows app and adapt it for Linux
        try:
            with open("ai_computer_agent.py", "r", encoding='utf-8') as f:
                windows_app = f.read()
                
            # Basic adaptations for Linux
            linux_app = windows_app.replace(
                "import psutil",
                "import psutil\nimport subprocess\nimport os"
            )
            
            # Add Linux-specific imports at the top
            linux_imports = """# Linux-specific imports
try:
    import pyautogui
    import pynput
    from pynput import mouse, keyboard
    pyautogui.FAILSAFE = True  # Enable failsafe for Linux
except ImportError:
    print("Warning: Some Linux automation libraries not available")

"""
            
            linux_app = linux_imports + linux_app
            
            with open(self.debian_dir / "usr/share/computer-use-agent/ai_computer_agent_linux.py", "w", encoding='utf-8') as f:
                f.write(linux_app)
                
        except FileNotFoundError:
            print("⚠️ Original app file not found, creating minimal Linux version")
            
            minimal_app = """#!/usr/bin/env python3
# Computer Use Agent - Linux Version

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from pathlib import Path

def main():
    root = tk.Tk()
    root.title("Computer Use Agent - Linux")
    root.geometry("600x400")
    
    # Main frame
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_label = ttk.Label(main_frame, text="Computer Use Agent", font=("Arial", 16, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Status
    status_label = ttk.Label(main_frame, text="Linux Version - Ready for Computer Vision Tasks")
    status_label.pack(pady=(0, 10))
    
    # Start button
    def start_agent():
        messagebox.showinfo("Computer Use Agent", "Computer Use Agent is starting...\nVision models loading...")
    
    start_button = ttk.Button(main_frame, text="Start Agent", command=start_agent)
    start_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
"""
            
            with open(self.debian_dir / "usr/share/computer-use-agent/ai_computer_agent_linux.py", "w", encoding='utf-8') as f:
                f.write(minimal_app)
                
        # Copy other necessary files
        for file in ["computer_agent.py", "setup_models.py"]:
            if Path(file).exists():
                shutil.copy2(file, self.debian_dir / f"usr/share/computer-use-agent/{file}")
                
        print("✅ Linux main application created")
        
    def create_documentation(self):
        """Create documentation files"""
        print("📝 Creating documentation...")
        
        readme_content = """Computer Use Agent for Linux
=============================

An AI-powered computer automation agent with vision capabilities.

Features:
- Visual screen understanding and analysis
- GUI element detection and interaction
- Natural language to computer actions
- Screenshot analysis and description
- Mouse and keyboard automation
- Multi-step task execution
- Error detection and correction

Usage:
------
Start from application menu: Applications → Utility → Computer Use Agent
Or run from terminal: computer-use-agent

Requirements:
------------
- Linux (Ubuntu/Mint/Debian)
- Python 3.8+
- X11 display server
- Internet connection (for initial model download)

Troubleshooting:
---------------
If the application doesn't start:
1. Ensure X11 is running: echo $DISPLAY
2. Check permissions: ls -la /usr/bin/computer-use-agent
3. Reinstall package: sudo apt install --reinstall ./computer-use-agent_1.0.0_amd64.deb

For support, visit: https://github.com/computeruse/agent
"""
        
        with open(self.debian_dir / "usr/share/doc/computer-use-agent/README", "w", encoding='utf-8') as f:
            f.write(readme_content)
            
        # Create changelog
        changelog_content = """computer-use-agent (1.0.0) stable; urgency=medium

  * Initial release for Linux
  * Computer vision and GUI automation capabilities
  * BLIP-2 vision model integration
  * PyAutoGUI and pynput automation support
  * Desktop integration with .desktop file
  * Debian package with proper dependencies

 -- Computer Use Agent Team <admin@computeruse.ai>  Thu, 06 Jun 2025 12:00:00 +0000
"""
        
        with open(self.debian_dir / "usr/share/doc/computer-use-agent/changelog", "w", encoding='utf-8') as f:
            f.write(changelog_content)
            
        # Create copyright file
        copyright_content = """Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: computer-use-agent
Upstream-Contact: Computer Use Agent Team <admin@computeruse.ai>

Files: *
Copyright: 2025 Computer Use Agent Team
License: MIT

License: MIT
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 .
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 .
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
"""
        
        with open(self.debian_dir / "usr/share/doc/computer-use-agent/copyright", "w", encoding='utf-8') as f:
            f.write(copyright_content)
            
        print("✅ Documentation created")
        
    def build_deb_package(self):
        """Build the final .deb package"""
        print("🔨 Building .deb package...")
        
        try:
            # Change to package directory
            os.chdir(self.package_dir)
            
            # Build the package using dpkg-deb
            deb_filename = f"{self.app_name}_{self.version}_amd64.deb"
            
            # Use fakeroot if available, otherwise try without
            build_commands = [
                ["fakeroot", "dpkg-deb", "--build", self.debian_dir.name, deb_filename],
                ["dpkg-deb", "--build", self.debian_dir.name, deb_filename]
            ]
            
            success = False
            for cmd in build_commands:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    success = True
                    print(f"✅ Package built successfully: {deb_filename}")
                    break
                except (subprocess.CalledProcessError, FileNotFoundError) as e:
                    continue
                    
            if not success:
                print("⚠️ dpkg-deb not available. Creating tar.gz instead...")
                # Create a tarball as fallback
                import tarfile
                with tarfile.open(f"{self.app_name}_{self.version}_linux.tar.gz", "w:gz") as tar:
                    tar.add(self.debian_dir.name, arcname=self.app_name)
                print(f"✅ Tarball created: {self.app_name}_{self.version}_linux.tar.gz")
                
            # Copy back to original directory
            os.chdir(self.project_dir)
            
            # Copy the built package to the main directory
            for ext in ['.deb', '_linux.tar.gz']:
                package_file = self.package_dir / f"{self.app_name}_{self.version}_amd64{ext}"
                if package_file.exists():
                    shutil.copy2(package_file, self.project_dir)
                    print(f"📦 Package copied to: {self.project_dir / package_file.name}")
                    
        except Exception as e:
            print(f"❌ Package build failed: {e}")
            return False
            
        return True
        
    def create_install_script(self):
        """Create installation script for systems without dpkg"""
        print("📝 Creating manual install script...")
        
        install_script = """#!/bin/bash
# Computer Use Agent - Manual Linux Installer

set -e

echo "Computer Use Agent - Linux Manual Installer"
echo "============================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or with sudo"
    exit 1
fi

# Check for required system packages
echo "Checking system dependencies..."
required_packages="python3 python3-pip python3-venv python3-tk x11-utils xdotool scrot"

for package in $required_packages; do
    if ! dpkg -l | grep -q "^ii  $package "; then
        echo "Installing $package..."
        apt-get update
        apt-get install -y $package
    fi
done

# Create directories
echo "Creating application directories..."
mkdir -p /usr/share/computer-use-agent
mkdir -p /usr/share/applications
mkdir -p /usr/share/icons/hicolor/64x64/apps
mkdir -p /usr/share/doc/computer-use-agent
mkdir -p /etc/computer-use-agent

# Copy files (assumes extracted package structure)
echo "Copying application files..."
cp -r usr/* /usr/
cp -r etc/* /etc/ 2>/dev/null || true

# Set permissions
chmod +x /usr/bin/computer-use-agent
chmod +x /usr/share/computer-use-agent/launch.sh

# Run post-install script
echo "Running post-installation setup..."
bash /usr/share/computer-use-agent/postinst.sh

echo "Installation completed successfully!"
echo "Start Computer Use Agent from applications menu or run 'computer-use-agent'"
"""
        
        install_script_path = self.package_dir / "install_linux.sh"
        with open(install_script_path, "w", encoding='utf-8') as f:
            f.write(install_script)
        install_script_path.chmod(0o755)
        
        # Copy postinst as separate script
        shutil.copy2(
            self.debian_dir / "DEBIAN/postinst",
            self.debian_dir / "usr/share/computer-use-agent/postinst.sh"
        )
        
        print("✅ Manual install script created")
        
    def create_linux_package(self):
        """Create complete Linux package"""
        print("🐧 Creating Linux .deb Package")
        print("=" * 40)
        
        # Clean and create structure
        self.clean_build_dirs()
        self.create_debian_structure()
        
        # Create package files
        self.create_control_file()
        self.create_postinst_script()
        self.create_prerm_script()
        self.create_desktop_file()
        self.create_icon()
        self.create_launcher_script()
        self.create_linux_setup_models()
        self.create_linux_main_app()
        self.create_documentation()
        self.create_install_script()
        
        # Build package
        if self.build_deb_package():
            print("\n🎉 Linux package created successfully!")
            print("\nInstallation options:")
            print(f"📦 Debian package: {self.app_name}_{self.version}_amd64.deb")
            print(f"🔧 Manual installer: install_linux.sh")
            print("\nTo install on Linux Mint/Ubuntu/Debian:")
            print(f"sudo dpkg -i {self.app_name}_{self.version}_amd64.deb")
            print("sudo apt-get install -f  # Fix any dependency issues")
            
        else:
            print("\n❌ Package creation failed")
            
if __name__ == "__main__":
    creator = LinuxPackageCreator()
    creator.create_linux_package()

