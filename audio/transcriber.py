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
