from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Optional
from datetime import date
import uuid

app = FastAPI(title="Mini Resume Management API")

# Database setup
DATABASE_URL = "sqlite:///./resumes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    dob = Column(String)
    contact_number = Column(String)
    contact_address = Column(String)
    education_qualification = Column(String)
    graduation_year = Column(Integer)
    years_of_experience = Column(Float)
    skill_set = Column(String)
    resume_filename = Column(String)

Base.metadata.create_all(bind=engine)


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/candidates")
def upload_candidate(
    full_name: str = Form(...),
    dob: date = Form(...),
    contact_number: str = Form(...),
    contact_address: str = Form(...),
    education_qualification: str = Form(...),
    graduation_year: int = Form(...),
    years_of_experience: float = Form(...),
    skill_set: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    candidate_id = str(uuid.uuid4())

    new_candidate = Candidate(
        id=candidate_id,
        full_name=full_name,
        dob=dob.isoformat(),
        contact_number=contact_number,
        contact_address=contact_address,
        education_qualification=education_qualification,
        graduation_year=graduation_year,
        years_of_experience=years_of_experience,
        skill_set=skill_set,
        resume_filename=resume.filename
    )

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return new_candidate


@app.get("/candidates")
def list_candidates(
    skill: Optional[str] = None,
    experience: Optional[float] = None,
    graduation_year: Optional[int] = None,
    db: Session = Depends(get_db)
):

    query = db.query(Candidate)

    if skill:
        query = query.filter(Candidate.skill_set.contains(skill))

    if experience is not None:
        query = query.filter(Candidate.years_of_experience >= experience)

    if graduation_year:
        query = query.filter(Candidate.graduation_year == graduation_year)

    return query.all()


@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: str, db: Session = Depends(get_db)):

    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return candidate


@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: str, db: Session = Depends(get_db)):

    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    db.delete(candidate)
    db.commit()

    return {"message": "Candidate deleted successfully"}