from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.resume import Resume
from app.models.job_description import JobDescription

from app.services.matcher import compute_match_score
from app.services.groq_advice import get_resume_improvements

router = APIRouter(prefix="/match", tags=["Matching"])


@router.get("/{resume_id}/{jd_id}")
def match_resume_jd(
    resume_id: int,
    jd_id: int,
    session: Session = Depends(get_session)
):
    resume = session.exec(select(Resume).where(Resume.id == resume_id)).first()
    jd = session.exec(select(JobDescription).where(
        JobDescription.id == jd_id)).first()

    if not resume or not jd:
        raise HTTPException(status_code=404, detail="Resume or JD not found")

    # ✅ Similarity score
    score = compute_match_score(resume.extracted_text, jd.jd_text)

    # ✅ Groq improvements
    advice = get_resume_improvements(resume.extracted_text, jd.jd_text)

    return {
        "match_score": score,
        "ai_suggestions": advice
    }
