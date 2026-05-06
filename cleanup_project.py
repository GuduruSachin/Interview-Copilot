import os

def cleanup():
    # Setup scripts to remove
    files_to_remove = [
        "bootstrap.py",
        "fix_project.py",
        "update_mock_flow.py",
        "fix_run_entry.py"
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Removed redundant script: {file}")
            except Exception as e:
                print(f"Failed to remove {file}: {e}")

    # Production run.py content
    run_py_content = """import os
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

    needs_restart = False
    for module_name, pip_name in required_packages.items():
        try:
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
    
    # Dynamically locate the interview_copilot folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.join(current_dir, "interview_copilot")
    
    # Add it to sys.path to allow absolute imports from within the app
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)

    try:
        from main import main as app_main
        app_main()
    except ImportError as e:
        print(f"Failed to load application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
    
    if os.path.exists("run.py"):
        with open("run.py", "w", encoding="utf-8") as f:
            f.write(run_py_content)
        print("Cleaned and finalized run.py.")

    # Ensure main.py is clean
    main_py_path = os.path.join("interview_copilot", "main.py")
    main_py_content = """import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    try:
        logger.info("Initializing Interview Copilot Application...")
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        logger.info("Application UI started successfully.")
        sys.exit(app.exec_())
    except Exception as e:
        logger.critical(f"Application failed to start: {e}")

if __name__ == "__main__":
    main()
"""
    
    if os.path.exists(main_py_path):
        with open(main_py_path, "w", encoding="utf-8") as f:
            f.write(main_py_content)
        print("Verified clean entry point in main.py.")

    print("Project cleaned and ready")

if __name__ == "__main__":
    cleanup()
