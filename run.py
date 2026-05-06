import os
import sys
import subprocess
import importlib.util

def check_and_install_packages():
    required_packages = {
        "PyQt5": "PyQt5",
        "pdfplumber": "pdfplumber",
        "numpy": "numpy",
        "sounddevice": "sounddevice",
        "faster_whisper": "faster-whisper",
        "google": "google-generativeai",
        "pydantic": "pydantic",
        "pydantic_settings": "pydantic-settings",
    }

    needs_restart = False
    for module_name, pip_name in required_packages.items():
        try:
            if module_name == "google":
                spec = importlib.util.find_spec("google.generativeai")
            else:
                spec = importlib.util.find_spec(module_name)
            
            if spec is None:
                raise ImportError
        except (ImportError, ValueError, AttributeError):
            print(f"Missing package '{pip_name}'. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
                needs_restart = True
            except subprocess.CalledProcessError as e:
                print(f"Error: Failed to install {pip_name}. Please install it manually. Details: {e}")
                sys.exit(1)
                
    if needs_restart:
        print("Packages installed successfully! Restarting the application...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

check_and_install_packages()

# Add the current root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from main import main

if __name__ == "__main__":
    main()
