
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List, Optional
from datetime import date
import uuid

app = FastAPI(title="Mini Resume Management API")

candidates = {}

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
    resume: UploadFile = File(...)
):
    candidate_id = str(uuid.uuid4())
    candidates[candidate_id] = {
        "id": candidate_id,
        "full_name": full_name,
        "dob": dob.isoformat(),
        "contact_number": contact_number,
        "contact_address": contact_address,
        "education_qualification": education_qualification,
        "graduation_year": graduation_year,
        "years_of_experience": years_of_experience,
        "skill_set": skill_set,
        "resume_filename": resume.filename
    }
    return candidates[candidate_id]

@app.get("/candidates")
def list_candidates(
    skill: Optional[str] = None,
    experience: Optional[float] = None,
    graduation_year: Optional[int] = None
):
    result = list(candidates.values())
    if skill:
        result = [c for c in result if skill.lower() in c["skill_set"].lower()]
    if experience is not None:
        result = [c for c in result if c["years_of_experience"] >= experience]
    if graduation_year:
        result = [c for c in result if c["graduation_year"] == graduation_year]
    return result

@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: str):
    if candidate_id not in candidates:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidates[candidate_id]

@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: str):
    if candidate_id not in candidates:
        raise HTTPException(status_code=404, detail="Candidate not found")
    del candidates[candidate_id]
    return {"message": "Candidate deleted successfully"}
