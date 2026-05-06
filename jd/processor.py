class JDProcessor:
    def __init__(self):
        pass

    def process(self, text: str) -> dict:
        return {
            "raw_text": text,
            "length": len(text)
        }
