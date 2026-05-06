from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel
from config.constants import APP_NAME
from core.session_manager import SessionManager
from utils.logger import get_logger

logger = get_logger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.session_manager = SessionManager()
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(800, 600)
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Status: Ready")
        self.transcript_area = QTextEdit()
        self.transcript_area.setPlaceholderText("Live transcript will appear here...")
        self.transcript_area.setReadOnly(True)
        
        self.start_btn = QPushButton("Start Session")
        self.start_btn.clicked.connect(self.on_start_session)
        self.stop_btn = QPushButton("Stop Recording")
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.transcript_area)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_start_session(self):
        self.status_label.setText("Status: Generating mock interview response...")
        self.transcript_area.append("-- Starting Mock Interview --")
        
        resume_sample = "Software Engineer with 10 years of Python experience."
        jd_sample = "Wanted: Senior Backend Engineer proficient in Python."
        question_sample = "Tell me about yourself"
        
        self.transcript_area.append(f"Question: {question_sample}")
        
        response = self.session_manager.run_mock_interview(
            resume_sample, 
            jd_sample, 
            question_sample
        )
        
        self.transcript_area.append(f"AI Response:\n{response}")
        self.transcript_area.append("----------------------------")
        self.status_label.setText("Status: Ready")
