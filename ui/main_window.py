from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QPushButton, 
                             QTextEdit, QLabel, QComboBox, QHBoxLayout, QFileDialog, QMessageBox, QStackedWidget)
from config.constants import APP_NAME
from core.session_manager import SessionManager
from utils.logger import get_logger

logger = get_logger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.session_manager = SessionManager()
        self.resume_path = ""
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(800, 700)
        
        self.stack = QStackedWidget()
        
        # Setup Screen
        self.setup_screen = QWidget()
        self.init_setup_screen()
        
        # Interview Screen
        self.interview_screen = QWidget()
        self.init_interview_screen()
        
        self.stack.addWidget(self.setup_screen)
        self.stack.addWidget(self.interview_screen)
        
        self.setCentralWidget(self.stack)
        self.stack.setCurrentWidget(self.setup_screen)

    def init_setup_screen(self):
        layout = QVBoxLayout()
        
        # Model Selection
        model_layout = QHBoxLayout()
        self.model_label = QLabel("Select Model:")
        self.model_dropdown = QComboBox()
        self.model_dropdown.addItems(self.session_manager.state.available_models)
        
        index = self.model_dropdown.findText(self.session_manager.state.selected_model)
        if index >= 0:
            self.model_dropdown.setCurrentIndex(index)
            
        self.model_dropdown.currentTextChanged.connect(self.on_model_change)
        
        model_layout.addWidget(self.model_label)
        model_layout.addWidget(self.model_dropdown)
        
        # Resume Upload
        resume_layout = QHBoxLayout()
        self.upload_btn = QPushButton("Upload Resume (PDF)")
        self.upload_btn.clicked.connect(self.on_upload_resume)
        self.resume_label = QLabel("No file selected")
        resume_layout.addWidget(self.upload_btn)
        resume_layout.addWidget(self.resume_label)
        
        # JD Input
        self.jd_label = QLabel("Job Description:")
        self.jd_area = QTextEdit()
        self.jd_area.setPlaceholderText("Paste Job Description here...")
        
        self.start_btn = QPushButton("Start Session")
        self.start_btn.clicked.connect(self.on_start_session)
        
        layout.addLayout(model_layout)
        layout.addLayout(resume_layout)
        layout.addWidget(self.jd_label)
        layout.addWidget(self.jd_area)
        layout.addWidget(self.start_btn)
        
        self.setup_screen.setLayout(layout)

    def init_interview_screen(self):
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Status: Ready")
        
        self.transcript_area = QTextEdit()
        self.transcript_area.setPlaceholderText("Live transcript will appear here...")
        self.transcript_area.setReadOnly(True)
        
        self.stop_btn = QPushButton("Stop Recording")
        self.stop_btn.clicked.connect(self.on_stop_session)
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.transcript_area)
        layout.addWidget(self.stop_btn)
        
        self.interview_screen.setLayout(layout)

    def on_model_change(self, selected_model: str):
        self.session_manager.state.selected_model = selected_model
        logger.info(f"Model changed to: {selected_model}")

    def on_upload_resume(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Resume", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            self.resume_path = file_path
            self.resume_label.setText(file_path.split("/")[-1])
            logger.info(f"Resume selected: {file_path}")

    def on_start_session(self):
        jd_text = self.jd_area.toPlainText().strip()
        
        if not self.resume_path:
            QMessageBox.warning(self, "Error", "Please upload a resume first.")
            return
            
        if not jd_text:
            QMessageBox.warning(self, "Error", "Please enter a Job Description.")
            return
            
        success = self.session_manager.start_session(self.resume_path, jd_text)
        if not success:
            QMessageBox.warning(self, "Error", "Failed to parse resume. Check logs.")
            return
            
        self.status_label.setText("Status: Listening...")
        self.transcript_area.clear()
        self.stack.setCurrentWidget(self.interview_screen)

    def on_stop_session(self):
        self.session_manager.stop_session()
        self.status_label.setText("Status: Ready")
        self.stack.setCurrentWidget(self.setup_screen)
