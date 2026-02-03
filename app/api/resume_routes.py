from fastapi import APIRouter, UploadFile, File, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.models.resume import Resume
from app.services.parser import extract_text_from_pdf

# ✅ Router must be defined BEFORE decorators
router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    # ✅ Read file bytes
    content = await file.read()

    # ✅ Extract clean text using PyMuPDF (not raw decode)
    extracted_text = extract_text_from_pdf(content)

    # ✅ Save to DB
    resume = Resume(
        filename=file.filename,
        extracted_text=extracted_text
    )

    session.add(resume)
    session.commit()
    session.refresh(resume)

    return {
        "message": "Resume uploaded and parsed ✅",
        "resume_id": resume.id,
        "preview": extracted_text[:300]
    }
