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
        "google.generativeai": "google-generativeai",
        "pydantic": "pydantic",
        "pydantic_settings": "pydantic-settings",
    }

    for module_name, pip_name in required_packages.items():
        if importlib.util.find_spec(module_name) is None:
            print(f"Missing package '{pip_name}'. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
            except subprocess.CalledProcessError as e:
                print(f"Error: Failed to install {pip_name}. Please install it manually. Details: {e}")
                sys.exit(1)

check_and_install_packages()

# Dynamically locate the interview_copilot folder
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "interview_copilot")

# Add it to sys.path to allow absolute imports from within the app
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from main import main

if __name__ == "__main__":
    main()
