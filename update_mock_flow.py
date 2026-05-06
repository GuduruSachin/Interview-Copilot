import os

def overwrite_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

def update_mock_flow():
    project_root = "interview_copilot"
    
    files = {
        os.path.join(project_root, "ui/main_window.py"): """
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
        
        self.transcript_area.append(f"AI Response:\\n{response}")
        self.transcript_area.append("----------------------------")
        self.status_label.setText("Status: Ready")
""",
        os.path.join(project_root, "core/session_manager.py"): """
from utils.logger import get_logger
from core.state import AppState
from ai.gemini_client import GeminiClient
from ai.prompt_builder import PromptBuilder

logger = get_logger(__name__)

class SessionManager:
    def __init__(self):
        self.state = AppState()
        self.gemini_client = GeminiClient()
        self.prompt_builder = PromptBuilder()
        logger.info("SessionManager initialized.")

    def start_session(self):
        self.state.is_running = True
        logger.info("Interview session has started.")

    def end_session(self):
        self.state.is_running = False
        logger.info("Interview session has ended.")

    def run_mock_interview(self, resume_text: str, jd_text: str, question: str) -> str:
        logger.info("Running mock interview flow.")
        prompt = self.prompt_builder.build_prompt(resume_text, jd_text, question)
        return self.gemini_client.get_suggestion(prompt)
""",
        os.path.join(project_root, "ai/prompt_builder.py"): """
class PromptBuilder:
    @staticmethod
    def build_interview_prompt(transcript: str, resume: str, jd: str) -> str:
        transcript = transcript.strip() if transcript else "N/A"
        resume = resume.strip()[:2000] if resume else "N/A"
        jd = jd.strip()[:2000] if jd else "N/A"
        
        return (
            "SYSTEM: You are an expert interview coach aiding a candidate in real-time.\\n"
            f"CANDIDATE RESUME: {resume}\\n"
            f"JOB DESCRIPTION: {jd}\\n"
            f"LIVE TRANSCRIPT: {transcript}\\n"
            "TASK: Provide a brief, actionable hint for the candidate."
        )

    @staticmethod
    def build_prompt(resume: str, jd: str, question: str) -> str:
        resume = resume.strip()[:2000] if resume else "N/A"
        jd = jd.strip()[:2000] if jd else "N/A"
        question = question.strip() if question else "N/A"
        
        return (
            "SYSTEM: You are an expert interview coach aiding a candidate in real-time.\\n"
            f"CANDIDATE RESUME: {resume}\\n"
            f"JOB DESCRIPTION: {jd}\\n"
            f"INTERVIEWER QUESTION: {question}\\n"
            "TASK: Provide a brief, professional, and actionable suggestion on how to answer."
        )
""",
        os.path.join(project_root, "ai/gemini_client.py"): """
import google.generativeai as genai
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class GeminiClient:
    def __init__(self):
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("GeminiClient successfully configured.")
        except Exception as e:
            logger.error(f"Failed to configure Gemini SDK: {e}")

    def get_suggestion(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text if response else "This is a sample response for testing."
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return "This is a sample response for testing."
"""
    }

    for path, content in files.items():
        overwrite_file(path, content)

    print("Mock flow ready")

if __name__ == "__main__":
    update_mock_flow()
