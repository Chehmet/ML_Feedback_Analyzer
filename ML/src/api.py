from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from .summary_generator import generate_summary
from .competency_scoring import evaluate_competencies
from .hard_skills_generator import extract_hard_skills
from .utils import get_list_useful_reviews, load_dotenv
import os


load_dotenv()
api = os.getenv("API_URL")
app = FastAPI()

class ReportRequest(BaseModel):
    worker_id: int
    reviews: Optional[List[str]] = None

class SummaryResponse(BaseModel):
    summary: str

class ReportResponse(BaseModel):
    competencies: List[dict]
    hard_skills: List[str]
    score: float

class ReviewsResponse(BaseModel):
    reviews: List[str]

def calculate_score(competencies):
    total_score = 0
    for competency in competencies:
        if competency['score']:
            total_score += competency['score']
    return total_score / len(competencies) if competencies else 0


@app.get("/get-reviews/{worker_id}", response_model=ReviewsResponse)
def get_reviews(worker_id: int):
    try:
        reviews = get_list_useful_reviews(worker_id)
        return {"reviews": reviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-summary", response_model=SummaryResponse)
def generate_summary_api(request: ReportRequest):
    reviews = request.reviews or get_list_useful_reviews(request.worker_id)
    try:
        summary = generate_summary(reviews, api)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-report", response_model=ReportResponse)
def generate_report_api(request: ReportRequest):
    reviews = request.reviews or get_list_useful_reviews(request.worker_id)
    try:
        competencies = evaluate_competencies(reviews, api)
        hard_skills = extract_hard_skills(reviews, api)
        score = calculate_score(competencies)

        return {
            "competencies": competencies,
            "hard_skills": hard_skills,
            "score": score
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
