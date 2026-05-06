import os

def overwrite_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

def fix_run_entry():
    run_py_content = """
import os
import sys

# Dynamically locate the interview_copilot folder
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "interview_copilot")

# Add it to sys.path to allow absolute imports from within the app
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from main import main

if __name__ == "__main__":
    main()
"""

    main_py_content = """
import sys
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

    overwrite_file("run.py", run_py_content)
    overwrite_file(os.path.join("interview_copilot", "main.py"), main_py_content)
    
    print("Run entry fixed")

if __name__ == "__main__":
    fix_run_entry()
