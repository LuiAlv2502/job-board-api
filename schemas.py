from datetime import datetime
from pydantic import BaseModel, EmailStr
 
 
# ---------- Job ----------
 
class JobBase(BaseModel):
    title: str
    company: str
    description: str | None = None
    location: str | None = None
 
 
class JobCreate(JobBase):
    pass
 
 
class JobOut(JobBase):
    id: int
    created_at: datetime
 
    model_config = {"from_attributes": True}
 
 
# ---------- Applicant ----------
 
class ApplicantBase(BaseModel):
    id: int
    name: str
    email: EmailStr
 
 
class ApplicantCreate(ApplicantBase):
    pass
 
 
class ApplicantOut(ApplicantBase):
    id: int
    created_at: datetime
 
    model_config = {"from_attributes": True}
 
 
# ---------- Application ----------
# Links an Applicant to a Job. References two other tables, so the
# "create" schema just needs the two foreign keys (status defaults on the model).
 
class ApplicationCreate(BaseModel):
    applicant_id: int
    job_id: int
 
 
class ApplicationOut(BaseModel):
    id: int
    applicant_id: int
    job_id: int
    status: str
    created_at: datetime
 
    model_config = {"from_attributes": True}