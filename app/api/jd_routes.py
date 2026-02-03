from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.models.job_description import JobDescription
from app.services.parser import extract_text_from_pdf

router = APIRouter(prefix="/jd", tags=["Job Description"])


@router.post("/upload")
async def upload_jd(
    jd_text: str = Form(None),                 # ✅ pasted JD
    jd_file: UploadFile = File(None),          # ✅ uploaded PDF
    session: Session = Depends(get_session)
):
    # ✅ Case 1: User pasted JD text
    if jd_text:
        final_text = jd_text

    # ✅ Case 2: User uploaded JD PDF
    elif jd_file:
        content = await jd_file.read()
        final_text = extract_text_from_pdf(content)

    # ❌ Nothing provided
    else:
        raise HTTPException(
            status_code=400,
            detail="Please provide either jd_text or jd_file"
        )

    # ✅ Save to DB
    jd = JobDescription(jd_text=final_text)

    session.add(jd)
    session.commit()
    session.refresh(jd)

    return {
        "message": "JD uploaded successfully ✅",
        "jd_id": jd.id,
        "preview": final_text[:300]
    }
