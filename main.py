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
