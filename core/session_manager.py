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
