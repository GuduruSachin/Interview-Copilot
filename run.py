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
        "google.genai": "google-genai>=0.5.0",
        "pydantic": "pydantic",
        "pydantic_settings": "pydantic-settings",
    }

    needs_restart = False
    for module_name, pip_name in required_packages.items():
        try:
            # specifically check google.genai since we migrated to it
            if module_name == "google.genai":
                spec = importlib.util.find_spec("google.genai")
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
                print(f"Error: Failed to install {pip_name}. Details: {e}")
                sys.exit(1)
                
    if needs_restart:
        print("Packages installed successfully! Restarting...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

def main():
    check_and_install_packages()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    try:
        from main import main as app_main
        app_main()
    except ImportError as e:
        print(f"Failed to load application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
