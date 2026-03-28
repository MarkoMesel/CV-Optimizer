from fastapi import FastAPI
from pydantic import BaseModel
import re

STOP_WORDS = {
    "a", "an", "the", "and", "or", "with", "for",
    "to", "in", "of", "i", "have", "looking"
}

app = FastAPI()

class AnalyzeRequest(BaseModel):
    cv_text: str
    job_description: str

def extract_keywords(text: str):
    # remove punctuation
    text = re.sub(r"[^\w\s#+.]", "", text.lower())
    words = set(text.split())
    return words - STOP_WORDS

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