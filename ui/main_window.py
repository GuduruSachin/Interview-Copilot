from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QPushButton, 
                             QTextEdit, QLabel, QComboBox, QHBoxLayout, QFileDialog, QMessageBox)
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
        self.jd_text = ""
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(800, 700)
        central_widget = QWidget()
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
        self.jd_area.setMaximumHeight(150)
        
        self.status_label = QLabel("Status: Ready")
        self.transcript_area = QTextEdit()
        self.transcript_area.setPlaceholderText("Live transcript will appear here...")
        self.transcript_area.setReadOnly(True)
        
        self.start_btn = QPushButton("Start Session")
        self.start_btn.clicked.connect(self.on_start_session)
        self.stop_btn = QPushButton("Stop Recording")
        
        layout.addLayout(model_layout)
        layout.addLayout(resume_layout)
        layout.addWidget(self.jd_label)
        layout.addWidget(self.jd_area)
        layout.addWidget(self.status_label)
        layout.addWidget(self.transcript_area)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

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
        self.jd_text = self.jd_area.toPlainText().strip()
        
        if not self.resume_path:
            QMessageBox.warning(self, "Error", "Please upload a resume first.")
            return
            
        if not self.jd_text:
            QMessageBox.warning(self, "Error", "Please enter a Job Description.")
            return
            
        self.status_label.setText("Status: Starting session...")
        self.transcript_area.append("-- Starting Session --")
        
        success = self.session_manager.start_session(self.resume_path, self.jd_text)
        if not success:
            self.status_label.setText("Status: Failed to start session")
            QMessageBox.warning(self, "Error", "Failed to parse resume. Check logs.")
            return
            
        self.status_label.setText("Status: Session active.")
        
        # Test question for mock flow using real data
        question = "Can you tell me how your experience in your resume align with this JD?"
        self.transcript_area.append(f"Question: {question}")
        
        response = self.session_manager.run_mock_interview(
            self.session_manager.state.resume_text, 
            self.session_manager.state.jd_text, 
            question
        )
        
        self.transcript_area.append(f"AI Response:\n{response}")
        self.transcript_area.append("----------------------------")
        self.status_label.setText("Status: Ready")
