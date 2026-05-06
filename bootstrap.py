import os
import sys

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

def bootstrap():
    project_root = "interview_copilot"
    
    # Define file contents
    files = {
        os.path.join(project_root, "main.py"): """
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info("Starting Interview Copilot Application")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

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
""",
        os.path.join(project_root, "config/settings.py"): """
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    WHISPER_MODEL: str = "base"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
""",
        os.path.join(project_root, "config/constants.py"): """
APP_NAME = "Interview Copilot"
OVERLAY_OPACITY = 0.8
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
""",
        os.path.join(project_root, "core/session_manager.py"): """
from utils.logger import get_logger
from core.state import AppState

logger = get_logger(__name__)

class SessionManager:
    def __init__(self):
        self.state = AppState()
        logger.info("Session Manager initialized")

    def start_session(self):
        self.state.is_running = True
        logger.info("Interview session started")

    def end_session(self):
        self.state.is_running = False
        logger.info("Interview session ended")
""",
        os.path.join(project_root, "core/context_manager.py"): """
from typing import Optional
from resume.parser import ResumeParser
from jd.processor import JDProcessor

class ContextManager:
    def __init__(self):
        self.resume_data = None
        self.jd_data = None

    def load_resume(self, file_path: str):
        parser = ResumeParser()
        self.resume_data = parser.extract_text(file_path)

    def load_jd(self, text: str):
        processor = JDProcessor()
        self.jd_data = processor.process(text)
""",
        os.path.join(project_root, "core/state.py"): """
from pydantic import BaseModel

class AppState(BaseModel):
    is_running: bool = False
    current_transcript: str = ""
    ai_suggestion: str = ""
""",
        os.path.join(project_root, "ai/gemini_client.py"): """
import google.generativeai as genai
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("Gemini Client initialized")

    async def get_suggestion(self, prompt: str) -> str:
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return "Error generating suggestion"
""",
        os.path.join(project_root, "ai/prompt_builder.py"): """
class PromptBuilder:
    @staticmethod
    def build_interview_prompt(transcript: str, resume: str, jd: str) -> str:
        return f\"\"\"
        Context: Interview in progress.
        Resume: {resume}
        Job Description: {jd}
        Latest Transcript: {transcript}
        
        Task: Provide a concise, professional suggestion or answer hint for the candidate.
        \"\"\"
""",
        os.path.join(project_root, "audio/recorder.py"): """
import sounddevice as sd
import numpy as np
from config.constants import SAMPLE_RATE
from utils.logger import get_logger

logger = get_logger(__name__)

class AudioRecorder:
    def __init__(self, callback):
        self.callback = callback
        self.stream = None

    def start(self):
        logger.info("Audio recording started")
        self.stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=self._audio_callback)
        self.stream.start()

    def _audio_callback(self, indata, frames, time, status):
        if status:
            logger.warning(f"Audio status: {status}")
        self.callback(indata.copy())

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            logger.info("Audio recording stopped")
""",
        os.path.join(project_root, "audio/transcriber.py"): """
from faster_whisper import WhisperModel
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class Transcriber:
    def __init__(self):
        self.model = WhisperModel(settings.WHISPER_MODEL, device="cpu", compute_type="int8")
        logger.info("Transcriber initialized with Whisper")

    def transcribe(self, audio_data):
        segments, info = self.model.transcribe(audio_data, beam_size=5)
        return " ".join([segment.text for segment in segments])
""",
        os.path.join(project_root, "resume/parser.py"): """
import pdfplumber
from utils.logger import get_logger

logger = get_logger(__name__)

class ResumeParser:
    def extract_text(self, file_path: str) -> str:
        logger.info(f"Extracting text from PDF: {file_path}")
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        except Exception as e:
            logger.error(f"Failed to parse PDF: {e}")
            return ""
""",
        os.path.join(project_root, "resume/extractor.py"): """
class EntityExtractor:
    def extract_skills(self, text: str):
        # Placeholder for skill extraction logic
        return []
""",
        os.path.join(project_root, "jd/processor.py"): """
class JDProcessor:
    def process(self, text: str) -> dict:
        # Placeholder for JD analysis logic
        return {"original_text": text}
""",
        os.path.join(project_root, "ui/main_window.py"): """
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from config.constants import APP_NAME

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        self.transcript_view = QTextEdit()
        self.transcript_view.setReadOnly(True)
        self.start_btn = QPushButton("Start Session")
        
        layout.addWidget(self.transcript_view)
        layout.addWidget(self.start_btn)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
""",
        os.path.join(project_root, "ui/overlay_window.py"): """
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from config.constants import OVERLAY_OPACITY

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(OVERLAY_OPACITY)
        
        layout = QVBoxLayout()
        self.suggestion_label = QLabel("Waiting for audio...")
        self.suggestion_label.setStyleSheet("color: white; font-size: 18px; background-color: rgba(0,0,0,150); padding: 10px;")
        layout.addWidget(self.suggestion_label)
        self.setLayout(layout)
""",
        os.path.join(project_root, "utils/logger.py"): """
import logging
import sys

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
""",
        os.path.join(project_root, "utils/helpers.py"): """
def format_timestamp(seconds: float) -> str:
    return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"
"""
    }

    # Create directories and files
    print("Creating project structure...")
    os.makedirs(os.path.join(project_root, "temp"), exist_ok=True)
    
    for path, content in files.items():
        create_file(path, content)
        print(f"Created: {path}")

    print("Project setup complete")

if __name__ == "__main__":
    bootstrap()
