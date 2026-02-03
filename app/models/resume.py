from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Resume(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    extracted_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
