from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db.session import engine
from app.api.resume_routes import router as resume_router

app = FastAPI(title="Resume AI Backend")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


app.include_router(resume_router)


@app.get("/")
def root():
    return {"message": "Resume AI Backend Running 🚀"}
