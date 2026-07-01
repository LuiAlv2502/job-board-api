from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    applications = relationship("Application", back_populates="applicant", cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    company = Column(String(150), nullable=False)
    description = Column(Text)
    location = Column(String(150))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("applicant_id", "job_id"),)

    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(30), nullable=False, default="submitted")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    applicant = relationship("Applicant", back_populates="applications")
    job = relationship("Job", back_populates="applications")