import os

def overwrite_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

def fix_project():
    project_root = "interview_copilot"
    
    files = {
        os.path.join(project_root, "main.py"): """
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
""",
        os.path.join(project_root, "requirements.txt"): """
python==3.11
PyQt5==5.15.10
faster-whisper==1.0.3
sounddevice==0.4.6
numpy==1.26.4
pdfplumber==0.10.3
google-generativeai==0.5.4
pydantic==2.7.1
pydantic-settings==2.2.1
""",
        os.path.join(project_root, "config/settings.py"): """
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str = Field("YOUR_API_KEY", env="GEMINI_API_KEY")
    WHISPER_MODEL: str = "base"
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
""",
        os.path.join(project_root, "config/constants.py"): """
APP_NAME = "Interview Copilot v1.0"
OVERLAY_OPACITY = 0.85
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
DEFAULT_PROMPT_LIMIT = 500
""",
        os.path.join(project_root, "core/session_manager.py"): """
from utils.logger import get_logger
from core.state import AppState

logger = get_logger(__name__)

class SessionManager:
    def __init__(self):
        self.state = AppState()
        logger.info("SessionManager initialized.")

    def start_session(self):
        self.state.is_running = True
        logger.info("Interview session has started.")

    def end_session(self):
        self.state.is_running = False
        logger.info("Interview session has ended.")
""",
        os.path.join(project_root, "core/context_manager.py"): """
from resume.parser import ResumeParser
from jd.processor import JDProcessor
from utils.logger import get_logger

logger = get_logger(__name__)

class ContextManager:
    def __init__(self):
        self.resume_text = ""
        self.jd_data = {}
        self.resume_parser = ResumeParser()
        self.jd_processor = JDProcessor()

    def set_resume(self, file_path: str):
        self.resume_text = self.resume_parser.extract_text(file_path)
        logger.info("Resume context updated.")

    def set_jd(self, text: str):
        self.jd_data = self.jd_processor.process(text)
        logger.info("JD context updated.")
""",
        os.path.join(project_root, "core/state.py"): """
from pydantic import BaseModel, Field

class AppState(BaseModel):
    is_running: bool = False
    current_transcript: str = ""
    ai_suggestion: str = ""
    error_message: str = ""
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

    def generate_suggestion(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text if response else "No suggestion generated."
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return "Suggestion unavailable due to API error."
""",
        os.path.join(project_root, "ai/prompt_builder.py"): """
class PromptBuilder:
    @staticmethod
    def build_interview_prompt(transcript: str, resume: str, jd: str) -> str:
        # Sanitization and safety check
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
""",
        os.path.join(project_root, "audio/recorder.py"): """
import numpy as np
import sounddevice as sd
from config.constants import SAMPLE_RATE
from utils.logger import get_logger

logger = get_logger(__name__)

class AudioRecorder:
    def __init__(self, callback):
        self.callback = callback
        self.stream = None

    def start(self):
        try:
            self.stream = sd.InputStream(
                samplerate=SAMPLE_RATE, 
                channels=1, 
                callback=self._audio_callback
            )
            self.stream.start()
            logger.info("Audio input stream started.")
        except Exception as e:
            logger.error(f"Could not start audio recording: {e}")

    def _audio_callback(self, indata, frames, time, status):
        if status:
            logger.warning(f"Audio stream status: {status}")
        self.callback(indata.copy())

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            logger.info("Audio input stream stopped.")
""",
        os.path.join(project_root, "audio/transcriber.py"): """
from faster_whisper import WhisperModel
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class Transcriber:
    def __init__(self):
        try:
            # Using CPU for better cross-platform stability in basic setups
            self.model = WhisperModel(settings.WHISPER_MODEL, device="cpu", compute_type="int8")
            logger.info(f"Whisper model '{settings.WHISPER_MODEL}' loaded.")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")

    def transcribe(self, audio_data: bytes) -> str:
        try:
            segments, _ = self.model.transcribe(audio_data)
            return " ".join([s.text for s in segments])
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return ""
""",
        os.path.join(project_root, "resume/parser.py"): """
import pdfplumber
from utils.logger import get_logger

logger = get_logger(__name__)

class ResumeParser:
    def extract_text(self, file_path: str) -> str:
        if not file_path.lower().endswith('.pdf'):
            logger.error("Only PDF files are supported for resume parsing.")
            return ""
            
        logger.info(f"Parsing PDF resume: {file_path}")
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    content = page.extract_text()
                    if content:
                        text += content + "\\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error parsing resume: {e}")
            return ""
""",
        os.path.join(project_root, "resume/extractor.py"): """
class EntityExtractor:
    def __init__(self):
        pass

    def extract_skills(self, text: str) -> list:
        # Implementation for skill pattern matching
        return []
""",
        os.path.join(project_root, "jd/processor.py"): """
class JDProcessor:
    def __init__(self):
        pass

    def process(self, text: str) -> dict:
        return {
            "raw_text": text,
            "length": len(text)
        }
""",
        os.path.join(project_root, "ui/main_window.py"): """
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel
from config.constants import APP_NAME

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(800, 600)
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Status: Ready")
        self.transcript_area = QTextEdit()
        self.transcript_area.setPlaceholderText("Live transcript will appear here...")
        self.transcript_area.setReadOnly(True)
        
        self.start_btn = QPushButton("Start Recording")
        self.stop_btn = QPushButton("Stop Recording")
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.transcript_area)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
""",
        os.path.join(project_root, "ui/overlay_window.py"): """
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from config.constants import OVERLAY_OPACITY

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_overlay()

    def init_overlay(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(OVERLAY_OPACITY)
        
        self.layout = QVBoxLayout()
        self.tip_label = QLabel("Waiting for context...")
        self.tip_label.setStyleSheet(\"\"\"
            background-color: rgba(30, 30, 30, 200);
            color: #00FF00;
            font-size: 16px;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #444;
        \"\"\")
        self.layout.addWidget(self.tip_label)
        self.setLayout(self.layout)
""",
        os.path.join(project_root, "utils/logger.py"): """
import logging
import sys

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
""",
        os.path.join(project_root, "utils/helpers.py"): """
import time

def get_current_timestamp() -> int:
    return int(time.time())

def clean_text(text: str) -> str:
    return " ".join(text.split())
"""
    }

    print("Initiating project refactor and bug fixes...")
    for path, content in files.items():
        overwrite_file(path, content)
        print(f"Fixed: {path}")

    print("Project fixed successfully")

if __name__ == "__main__":
    fix_project()
