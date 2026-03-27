from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AnalyzeRequest(BaseModel):
    cv_text: str
    job_description: str


def extract_keywords(text: str):
    return set(text.lower().split())

@app.get("/")
def read_root():
    return {"message": "CV-Optimizer API is running"}

@app.post("/analyze")
def analyze(data: AnalyzeRequest):
    cv_words = extract_keywords(data.cv_text)
    job_words = extract_keywords(data.job_description)

    matched = cv_words.intersection(job_words)
    missing = job_words - cv_words

    score = int((len(matched) / len(job_words)) * 100) if job_words else 0

    return {
        "match_score": score,
        "matched_keywords": list(matched),
        "missing_keywords": list(missing)
    }