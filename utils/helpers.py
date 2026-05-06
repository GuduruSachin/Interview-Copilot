import time

def get_current_timestamp() -> int:
    return int(time.time())

def clean_text(text: str) -> str:
    return " ".join(text.split())
