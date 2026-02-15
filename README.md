
# Mini Resume Management API

## Python Version
Python 3.10+

## Installation Steps
```bash
git clone https://github.com/deons-dennis/miniresume-your-full-name.git
cd miniresume-your-full-name
pip install -r requirements.txt
```

## Run the Application
```bash
uvicorn main:app --reload
```

## Health Check
GET /health

Response:
```json
{ "status": "ok" }
```

## Upload Candidate
POST /candidates (form-data)

Fields:
- full_name
- dob
- contact_number
- contact_address
- education_qualification
- graduation_year
- years_of_experience
- skill_set
- resume (file)

## Example Response
```json
{
  "id": "uuid",
  "full_name": "John Doe",
  "graduation_year": 2022,
  "years_of_experience": 2.5,
  "skill_set": "Python, FastAPI"
}
```
