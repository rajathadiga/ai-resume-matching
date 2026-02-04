import os
from llama_index.llms.groq import Groq

llm = Groq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


def get_resume_improvements(resume_text: str, jd_text: str) -> str:
    prompt = f"""
You are an ATS resume expert.

Resume:
{resume_text}

Job Description:
{jd_text}

Give:
1. Missing skills
2. Improvements
3. Short shortlist probability reasoning
Return clearly in bullet points.
"""

    response = llm.complete(prompt)
    return response.text
