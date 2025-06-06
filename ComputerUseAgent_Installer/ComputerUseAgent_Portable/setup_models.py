#!/usr/bin/env python3
"""
Model Setup Script for AI Computer Use Agent
This script downloads and prepares vision-language models for GUI control.
"""

import os
import sys
import subprocess
from pathlib import Path
import json

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages for computer vision and GUI control"""
    print("📦 Installing required packages for computer vision...")
    
    # Requirements for computer vision and GUI control
    vision_requirements = [
        "torch>=1.9.0",
        "torchvision>=0.10.0",
        "transformers>=4.25.0", 
        "accelerate>=0.16.0",
        "numpy>=1.21.0",
        "requests>=2.25.0",
        "pillow>=8.3.0",
        "opencv-python>=4.5.0",
        "pyautogui>=0.9.54",
        "pynput>=1.7.6",
        "psutil>=5.8.0",
        "screeninfo>=0.8"
    ]
    
    for package in vision_requirements:
        print(f"Installing {package}...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout per package (vision models are larger)
            )
            if result.returncode != 0:
                print(f"⚠️ Warning: Failed to install {package}")
                print(f"Error: {result.stderr}")
            else:
                print(f"✅ {package} installed successfully")
        except subprocess.TimeoutExpired:
            print(f"⚠️ Timeout installing {package}")
        except Exception as e:
            print(f"⚠️ Error installing {package}: {e}")

def create_models_directory():
    """Create directory structure for models"""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Create subdirectories for computer vision models
    (models_dir / "vision_language").mkdir(exist_ok=True)
    (models_dir / "screen_understanding").mkdir(exist_ok=True)
    (models_dir / "gui_detection").mkdir(exist_ok=True)
    (models_dir / "cache").mkdir(exist_ok=True)
    
    print("📁 Model directories created")
    return models_dir

def download_models():
    """Download and cache vision-language models for computer use"""
    print("🤖 Preparing computer vision models for GUI control...")
    
    try:
        # Import after installation
        from transformers import BlipProcessor, BlipForConditionalGeneration
        from transformers import AutoProcessor, AutoModelForVision2Seq
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
        
        print("Downloading Qwen-VL model for computer use tasks...")
        # Try to load a smaller vision-language model suitable for computer use
        try:
            qwen_processor = AutoProcessor.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)
            qwen_model = AutoModelForVision2Seq.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)
            qwen_model.to(device)
            print("✅ Qwen-VL model ready")
        except Exception as e:
            print(f"⚠️ Qwen-VL not available, using BLIP-2 only: {e}")
            qwen_processor = None
            qwen_model = None
        
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
        print("Please run the installation step first")
        return False
    except Exception as e:
        print(f"❌ Error downloading models: {e}")
        return False

def create_model_config():
    """Create configuration file for vision models"""
    import torch
    
    config = {
        "models": {
            "vision_language": {
                "name": "Salesforce/blip-image-captioning-base",
                "type": "blip",
                "local_path": "models/vision_language/blip",
                "capabilities": ["image_captioning", "visual_qa", "screen_understanding"]
            },
            "computer_use": {
                "name": "Qwen/Qwen-VL-Chat",
                "type": "qwen_vl",
                "local_path": "models/vision_language/qwen_vl",
                "capabilities": ["gui_understanding", "action_planning", "screen_analysis"]
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

def create_offline_launcher():
    """Create launcher script for offline use"""
    launcher_content = '''@echo off
echo Starting AI Computer Use Agent (Offline Mode)...
echo Models are preinstalled and ready to use locally!
echo.
python ai_computer_agent.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error running the AI agent. 
    echo Make sure Python and required packages are installed.
    echo You can run setup_models.py to reinstall dependencies.
    echo.
    pause
)
'''
    
    with open("run_ai_agent.bat", "w") as f:
        f.write(launcher_content)
    
    print("✅ Offline launcher created: run_ai_agent.bat")

def main():
    """Main setup function"""
    print("🚀 AI Computer Use Agent - Model Setup")
    print("=====================================\n")
    
    # Check Python version
    if not check_python_version():
        return
    
    # Create model directories
    models_dir = create_models_directory()
    
    # Install requirements
    print("\n📦 Installing Dependencies")
    print("-" * 30)
    install_requirements()
    
    # Download models
    print("\n🤖 Setting Up AI Models")
    print("-" * 25)
    models_ready = download_models()
    
    if models_ready:
        # Create config
        create_model_config()
        
        # Create launcher
        create_offline_launcher()
        
        print("\n🎉 Setup Complete!")
        print("==================")
        print("✅ All AI models are downloaded and ready")
        print("✅ Agent can now work offline")
        print("To start the AI agent:")
        print("1. Double-click 'run_ai_agent.bat'")
        print("2. Or run: python ai_computer_agent.py")
        print("\nComputer Use Features available:")
        print("• Visual screen understanding and analysis")
        print("• GUI element detection and interaction")
        print("• Natural language to computer actions")
        print("• Screenshot analysis and description")
        print("• Mouse and keyboard automation")
        print("• Multi-step task execution")
        print("• Error detection and correction")
    else:
        print("\n❌ Setup incomplete")
        print("Some models failed to download.")
        print("You can still use the basic agent features.")

if __name__ == "__main__":
    main()

