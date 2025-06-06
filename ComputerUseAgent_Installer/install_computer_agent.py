#!/usr/bin/env python3
"""
Computer Use Agent - Self-Installing Package
This script downloads and installs all dependencies automatically.
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import json
from pathlib import Path
import tempfile
import shutil

class AutoInstaller:
    def __init__(self):
        self.install_dir = Path.cwd() / "ComputerUseAgent"
        self.python_exe = None
        
    def check_python(self):
        """Check if Python 3.8+ is available"""
        try:
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True)
            version = result.stdout.strip()
            print(f"✅ Found {version}")
            
            # Check version
            version_parts = version.split()[1].split('.')
            major, minor = int(version_parts[0]), int(version_parts[1])
            
            if major >= 3 and minor >= 8:
                self.python_exe = sys.executable
                return True
            else:
                print("❌ Python 3.8+ required")
                return False
                
        except Exception as e:
            print(f"❌ Python not found: {e}")
            return self.install_python()
            
    def install_python(self):
        """Download and install Python if not available"""
        print("📥 Downloading Python 3.11...")
        
        python_url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
        installer_path = Path(tempfile.gettempdir()) / "python_installer.exe"
        
        try:
            urllib.request.urlretrieve(python_url, installer_path)
            print("🔧 Installing Python (this may take a few minutes)...")
            
            # Silent install with add to PATH
            result = subprocess.run([
                str(installer_path), 
                "/quiet", 
                "InstallAllUsers=1", 
                "PrependPath=1",
                "Include_test=0"
            ], check=True)
            
            # Update PATH for current session
            python_path = "C:\Program Files\Python311"
            if Path(python_path).exists():
                os.environ["PATH"] = f"{python_path};{python_path}\Scripts;{os.environ['PATH']}"
                self.python_exe = f"{python_path}\python.exe"
                return True
            else:
                # Try user installation
                user_python = Path.home() / "AppData/Local/Programs/Python/Python311"
                if user_python.exists():
                    self.python_exe = str(user_python / "python.exe")
                    return True
                    
        except Exception as e:
            print(f"❌ Failed to install Python: {e}")
            return False
            
    def install_dependencies(self):
        """Install all required packages"""
        print("📦 Installing dependencies...")
        
        packages = [
            "torch>=1.9.0",
            "torchvision>=0.10.0", 
            "transformers>=4.25.0",
            "accelerate>=0.16.0",
            "numpy>=1.21.0",
            "pillow>=8.3.0",
            "opencv-python>=4.5.0",
            "pyautogui>=0.9.54",
            "pynput>=1.7.6",
            "screeninfo>=0.8",
            "psutil>=5.8.0",
            "requests>=2.25.0"
        ]
        
        for package in packages:
            print(f"Installing {package}...")
            try:
                subprocess.run([
                    self.python_exe, "-m", "pip", "install", package, "--user"
                ], check=True, capture_output=True)
                print(f"✅ {package} installed")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Warning: {package} failed to install")
                
    def download_models(self):
        """Download AI models"""
        print("🤖 Setting up AI models...")
        
        setup_script = """
import sys
sys.path.insert(0, ".")
from setup_models import download_models
download_models()
"""
        
        try:
            with open("temp_setup.py", "w") as f:
                f.write(setup_script)
                
            subprocess.run([self.python_exe, "temp_setup.py"], check=True)
            os.remove("temp_setup.py")
            print("✅ Models downloaded successfully")
            
        except Exception as e:
            print(f"⚠️ Model download failed: {e}")
            
    def create_shortcuts(self):
        """Create desktop shortcuts"""
        print("🔗 Creating shortcuts...")
        
        try:
            # Create batch file for easy launching
            batch_content = f"""@echo off
cd /d "{self.install_dir}"
"{self.python_exe}" ai_computer_agent.py
pause
"""
            
            with open(self.install_dir / "Launch_Computer_Agent.bat", "w") as f:
                f.write(batch_content)
                
            print("✅ Launch script created")
            
        except Exception as e:
            print(f"⚠️ Shortcut creation failed: {e}")
            
    def install(self):
        """Main installation process"""
        print("🚀 Computer Use Agent Installer")
        print("=" * 40)
        
        # Create installation directory
        self.install_dir.mkdir(exist_ok=True)
        os.chdir(self.install_dir)
        
        # Check/install Python
        if not self.check_python():
            print("❌ Python installation failed")
            return False
            
        # Copy source files
        print("📁 Copying application files...")
        source_files = [
            "ai_computer_agent.py",
            "computer_agent.py", 
            "setup_models.py"
        ]
        
        for file in source_files:
            if Path(f"../{file}").exists():
                shutil.copy2(f"../{file}", file)
                
        # Install dependencies
        self.install_dependencies()
        
        # Download models
        self.download_models()
        
        # Create shortcuts
        self.create_shortcuts()
        
        print("
🎉 Installation Complete!")
        print(f"📁 Installed to: {self.install_dir}")
        print("🚀 Run 'Launch_Computer_Agent.bat' to start")
        
        return True

if __name__ == "__main__":
    installer = AutoInstaller()
    installer.install()
    input("
Press Enter to exit...")
