from fastapi import FastAPI
from sqlmodel import SQLModel

from app.db.session import engine
from app.api.resume_routes import router as resume_router
from app.api.jd_routes import router as jd_router
from app.api.match_routes import router as match_router


# ✅ FIRST create the FastAPI app
app = FastAPI(title="Resume AI Backend")

# ✅ Startup event (create tables)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# ✅ THEN include routers
app.include_router(resume_router)
app.include_router(jd_router)
app.include_router(match_router)

# ✅ Test route


@app.get("/")
def root():
    return {"message": "Backend running ✅"}
