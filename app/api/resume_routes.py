from fastapi import APIRouter, UploadFile, File
from sqlmodel import Session
from app.db.session import get_session
from app.models.resume import Resume

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    text = await file.read()

    resume = Resume(
        filename=file.filename,
        extracted_text=text.decode(errors="ignore")
    )

    return {
        "status": "uploaded",
        "filename": resume.filename
    }
