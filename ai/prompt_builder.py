class PromptBuilder:
    @staticmethod
    def build_interview_prompt(transcript: str, resume: str, jd: str) -> str:
        transcript = transcript.strip() if transcript else "N/A"
        resume = resume.strip()[:2000] if resume else "N/A"
        jd = jd.strip()[:2000] if jd else "N/A"
        
        return (
            "SYSTEM: You are an expert interview coach aiding a candidate in real-time.\n"
            f"CANDIDATE RESUME: {resume}\n"
            f"JOB DESCRIPTION: {jd}\n"
            f"LIVE TRANSCRIPT: {transcript}\n"
            "TASK: Provide a brief, actionable hint for the candidate."
        )

    @staticmethod
    def build_prompt(resume: str, jd: str, question: str) -> str:
        resume = resume.strip()[:2000] if resume else "N/A"
        jd = jd.strip()[:2000] if jd else "N/A"
        question = question.strip() if question else "N/A"
        
        return (
            "SYSTEM: You are an expert interview coach aiding a candidate in real-time.\n"
            f"CANDIDATE RESUME: {resume}\n"
            f"JOB DESCRIPTION: {jd}\n"
            f"INTERVIEWER QUESTION: {question}\n"
            "TASK: Provide a brief, professional, and actionable suggestion on how to answer."
        )
