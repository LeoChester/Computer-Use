#!/usr/bin/env python3
"""
Computer Use Agent - Complete Installer Creator
This script creates a single executable installer that includes all dependencies.
"""

import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path
import json
import requests

class InstallerCreator:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.build_dir = self.project_dir / "build"
        self.dist_dir = self.project_dir / "dist"
        self.installer_dir = self.project_dir / "installer_files"
        
    def clean_build_dirs(self):
        """Clean previous build directories"""
        print("🧹 Cleaning build directories...")
        for dir_path in [self.build_dir, self.dist_dir, self.installer_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
        
        # Create fresh directories
        self.installer_dir.mkdir(exist_ok=True)
        
    def create_embedded_installer(self):
        """Create a self-contained installer script"""
        print("📦 Creating embedded installer...")
        
        installer_script = '''#!/usr/bin/env python3
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
            python_path = "C:\\Program Files\\Python311"
            if Path(python_path).exists():
                os.environ["PATH"] = f"{python_path};{python_path}\\Scripts;{os.environ['PATH']}"
                self.python_exe = f"{python_path}\\python.exe"
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
        
        print("\n🎉 Installation Complete!")
        print(f"📁 Installed to: {self.install_dir}")
        print("🚀 Run 'Launch_Computer_Agent.bat' to start")
        
        return True

if __name__ == "__main__":
    installer = AutoInstaller()
    installer.install()
    input("\nPress Enter to exit...")
'''
        
        # Write the installer script
        installer_path = self.installer_dir / "install_computer_agent.py"
        with open(installer_path, "w", encoding='utf-8') as f:
            f.write(installer_script)
            
        print(f"✅ Created installer: {installer_path}")
        
    def create_portable_package(self):
        """Create a portable zip package"""
        print("📦 Creating portable package...")
        
        # Create portable directory structure
        portable_dir = self.installer_dir / "ComputerUseAgent_Portable"
        portable_dir.mkdir(exist_ok=True)
        
        # Copy application files
        app_files = [
            "ai_computer_agent.py",
            "computer_agent.py",
            "setup_models.py",
            "model_config.json"
        ]
        
        for file in app_files:
            if Path(file).exists():
                shutil.copy2(file, portable_dir / file)
                
        # Create portable installer
        portable_installer = '''@echo off
echo Computer Use Agent - Portable Setup
echo ===================================
echo.
echo This will install Python and dependencies if needed...
echo.
pause

python install_computer_agent.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Python not found. Downloading installer...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe'"
    echo Running Python installer...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    echo.
    echo Please restart this installer after Python installation completes.
    pause
    exit
)
'''
        
        with open(portable_dir / "INSTALL.bat", "w", encoding='utf-8') as f:
            f.write(portable_installer)
            
        # Copy installer script
        shutil.copy2(
            self.installer_dir / "install_computer_agent.py",
            portable_dir / "install_computer_agent.py"
        )
        
        # Create zip package
        zip_path = self.installer_dir / "ComputerUseAgent_Portable.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in portable_dir.rglob('*'):
                if file_path.is_file():
                    arc_path = file_path.relative_to(portable_dir)
                    zf.write(file_path, arc_path)
                    
        print(f"✅ Created portable package: {zip_path}")
        
    def create_exe_installer(self):
        """Create single EXE installer using PyInstaller"""
        print("🔧 Creating EXE installer...")
        
        try:
            # Create a consolidated installer script
            exe_installer_script = self.installer_dir / "exe_installer.py"
            
            with open(exe_installer_script, "w", encoding='utf-8') as f:
                f.write('''
import os
import sys
import subprocess
import tempfile
import zipfile
from pathlib import Path
import urllib.request
import shutil

# Embedded application files (base64 encoded)
APP_FILES = {
''')
                
                # Embed application files as base64
                import base64
                app_files = ["ai_computer_agent.py", "computer_agent.py", "setup_models.py"]
                
                for file in app_files:
                    if Path(file).exists():
                        with open(file, 'rb') as rf:
                            content = base64.b64encode(rf.read()).decode('utf-8')
                            f.write(f'    "{file}": "{content}",\n')
                            
                f.write('''
}

def extract_files(target_dir):
    """Extract embedded files"""
    import base64
    target_dir = Path(target_dir)
    target_dir.mkdir(exist_ok=True)
    
    for filename, content in APP_FILES.items():
        file_path = target_dir / filename
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(content.encode('utf-8')))
    
    print(f"✅ Extracted files to {target_dir}")

# Include the AutoInstaller class here...
''')
                
            # Build EXE
            result = subprocess.run([
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--windowed",
                "--name", "ComputerUseAgent_Installer",
                "--distpath", str(self.installer_dir),
                str(exe_installer_script)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ EXE installer created successfully")
            else:
                print(f"⚠️ EXE creation failed: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️ EXE creation failed: {e}")
            
    def copy_to_d_drive(self):
        """Copy installer files to D drive"""
        try:
            d_drive_path = Path("D:/ComputerUseAgent_Installer")
            d_drive_path.mkdir(exist_ok=True)
            
            # Copy all installer files
            for file_path in self.installer_dir.rglob('*'):
                if file_path.is_file():
                    rel_path = file_path.relative_to(self.installer_dir)
                    dest_path = d_drive_path / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest_path)
                    
            print(f"✅ Installer files copied to {d_drive_path}")
            
            # Create simple install script on D drive
            install_script = f'''@echo off
cd /d "{d_drive_path}"
echo Computer Use Agent - Quick Install
echo ==================================
echo.
echo Installing from D drive...
echo.
if exist "ComputerUseAgent_Portable.zip" (
    echo Extracting portable package...
    powershell -Command "Expand-Archive -Path 'ComputerUseAgent_Portable.zip' -DestinationPath 'C:\\ComputerUseAgent' -Force"
    cd /d "C:\\ComputerUseAgent"
    call INSTALL.bat
) else (
    echo Running Python installer...
    python install_computer_agent.py
)
echo.
echo Installation complete!
pause
'''
            
            with open(d_drive_path / "QUICK_INSTALL.bat", "w", encoding='utf-8') as f:
                f.write(install_script)
                
            print("🚀 D Drive installer ready! Run QUICK_INSTALL.bat from D drive")
            
        except Exception as e:
            print(f"⚠️ D drive copy failed: {e}")
            
    def create_all_installers(self):
        """Create all installer types"""
        print("🏗️ Creating Complete Installer Package")
        print("=" * 50)
        
        # Clean previous builds
        self.clean_build_dirs()
        
        # Create different installer types
        self.create_embedded_installer()
        self.create_portable_package()
        self.create_exe_installer()
        self.copy_to_d_drive()
        
        print("\n🎉 All installers created!")
        print("\nInstaller Options:")
        print(f"📁 Portable ZIP: {self.installer_dir / 'ComputerUseAgent_Portable.zip'}")
        print(f"🐍 Python Script: {self.installer_dir / 'install_computer_agent.py'}")
        print(f"💾 D Drive: D:/ComputerUseAgent_Installer/QUICK_INSTALL.bat")
        
if __name__ == "__main__":
    creator = InstallerCreator()
    creator.create_all_installers()

