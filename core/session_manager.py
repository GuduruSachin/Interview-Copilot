from utils.logger import get_logger
from core.state import AppState
from ai.gemini_client import GeminiClient
from ai.prompt_builder import PromptBuilder
from resume.parser import ResumeParser
from jd.processor import JDProcessor

logger = get_logger(__name__)

class SessionManager:
    def __init__(self):
        self.state = AppState()
        self.gemini_client = GeminiClient()
        self.prompt_builder = PromptBuilder()
        self.resume_parser = ResumeParser()
        self.jd_processor = JDProcessor()
        logger.info("SessionManager initialized.")
        self._init_models()

    def _init_models(self):
        models = self.gemini_client.get_available_models()
        self.state.available_models = models
        if models:
            self.state.selected_model = self.gemini_client.get_best_latency_model(models)

    def start_session(self, resume_path: str, jd_text: str) -> bool:
        logger.info("Extracting resume text...")
        resume_text = self.resume_parser.extract_text(resume_path)
        if not resume_text:
            logger.error("Failed to extract text from resume.")
            return False
            
        logger.info("Processing JD...")
        jd_data = self.jd_processor.process(jd_text)
        
        self.state.resume_text = resume_text
        self.state.jd_text = jd_data.get("raw_text", jd_text)
        
        self.state.is_running = True
        logger.info("Interview session has started.")
        return True

    def stop_session(self):
        self.state.is_running = False
        logger.info("Interview session has ended.")

    def run_mock_interview(self, resume_text: str, jd_text: str, question: str) -> str:
        logger.info("Running mock interview flow.")
        prompt = self.prompt_builder.build_prompt(resume_text, jd_text, question)
        return self.gemini_client.get_suggestion(prompt, self.state.selected_model)
