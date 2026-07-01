from typing_extensions import Annotated

from fastapi import FastAPI, HTTPException, Depends
from database import init_db
import models 
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from schemas import ApplicantCreate, ApplicantOut, JobCreate, JobOut, ApplicationCreate, ApplicationOut

app = FastAPI()

@app.on_event("startup")
def on_startup() -> None:
    init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/applicants/", response_model=ApplicantOut)
def create_applicant(applicant: ApplicantCreate, db: db_dependency):
    db_applicant = models.Applicant(id=applicant.id, name=applicant.name, email=applicant.email)
    db.add(db_applicant)
    db.commit()
    db.refresh(db_applicant)
    return db_applicant

@app.get("/applicants/{applicant_id}", response_model=ApplicantOut)
def get_applicant(applicant_id: int, db: db_dependency):
    db_applicant = db.query(models.Applicant).filter(models.Applicant.id == applicant_id).first()
    if db_applicant is None:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return db_applicant

@app.post("/job/", response_model=JobOut)
def create_job(job: JobCreate, db: db_dependency):
    db_job = models.Job(title=job.title, company=job.company, description=job.description, location=job.location)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs/", response_model=list[JobOut])
def list_jobs(db: db_dependency):
    jobs = db.query(models.Job).all()
    return jobs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)