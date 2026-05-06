from google import genai
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class GeminiClient:
    def __init__(self):
        try:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            logger.info("GeminiClient successfully configured using google-genai.")
        except Exception as e:
            logger.error(f"Failed to configure Gemini SDK: {e}")
            self.client = None

    def get_available_models(self) -> list:
        if not self.client:
            logger.warning("Client not initialized. Falling back to default model.")
            return ["gemini-1.5-flash"]
        try:
            models_info = self.client.models.list()
            available = []
            for m in models_info:
                # Provide a fallback since structure might vary
                actions = getattr(m, 'supported_actions', [])
                if not actions or 'generateContent' in actions:
                    name = m.name.replace('models/', '') if m.name.startswith('models/') else m.name
                    available.append(name)
            return available if available else ["gemini-1.5-flash"]
        except Exception as e:
            logger.error(f"Failed to fetch models: {e}")
            return ["gemini-1.5-flash"]

    def get_best_latency_model(self, models: list) -> str:
        for m in models:
            if "flash" in str(m).lower():
                return str(m)
        return str(models[0]) if models else "gemini-1.5-flash"

    def get_suggestion(self, prompt: str, model_name: str = "gemini-1.5-flash") -> str:
        if not self.client:
            return "This is a sample response for testing (API client failed to initialize)."
        try:
            response = self.client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text if response else "This is a sample response for testing."
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return "This is a sample response for testing."
