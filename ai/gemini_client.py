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
