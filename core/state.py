from pydantic import BaseModel, Field

class AppState(BaseModel):
    is_running: bool = False
    current_transcript: str = ""
    ai_suggestion: str = ""
    error_message: str = ""
