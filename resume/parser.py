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
                        text += content + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error parsing resume: {e}")
            return ""
