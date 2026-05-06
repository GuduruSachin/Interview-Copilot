from resume.parser import ResumeParser
from jd.processor import JDProcessor
from utils.logger import get_logger

logger = get_logger(__name__)

class ContextManager:
    def __init__(self):
        self.resume_text = ""
        self.jd_data = {}
        self.resume_parser = ResumeParser()
        self.jd_processor = JDProcessor()

    def set_resume(self, file_path: str):
        self.resume_text = self.resume_parser.extract_text(file_path)
        logger.info("Resume context updated.")

    def set_jd(self, text: str):
        self.jd_data = self.jd_processor.process(text)
        logger.info("JD context updated.")
