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
    """
    Модель запроса для генерации отчета.
    
    Атрибуты:
    - worker_id (int): ID сотрудника
    - reviews (Optional[List[str]]): список отзывов (опционально)
    """
    worker_id: int
    reviews: Optional[List[str]] = None

class SummaryResponse(BaseModel):
    """
    Модель ответа для сводки.
    
    Атрибуты:
    - summary (str): текст сводки
    """
    summary: str

class ReportResponse(BaseModel):
    """
    Модель ответа для полного отчета.
    
    Атрибуты:
    - competencies (List[dict]): список оценок компетенций
    - hard_skills (List[str]): список выявленных технических навыков
    - score (float): общий балл
    """
    competencies: List[dict]
    hard_skills: List[str]
    score: float

class ReviewsResponse(BaseModel):
    """
    Модель ответа для списка отзывов.
    
    Атрибуты:
    - reviews (List[str]): список отзывов
    """
    reviews: List[str]

def calculate_score(competencies):
    """
    Рассчитывает средний балл на основе оценок компетенций.
    
    Аргументы:
    - competencies (List[dict]): список словарей с оценками компетенций
    
    Возвращает:
    float: средний балл
    """
    total_score = 0
    for competency in competencies:
        if competency['score']:
            total_score += competency['score']
    return total_score / len(competencies) if competencies else 0


@app.get("/get-reviews/{worker_id}", response_model=ReviewsResponse)
def get_reviews(worker_id: int):
    """
    Получает список отзывов для указанного сотрудника.
    
    Аргументы:
    - worker_id (int): ID сотрудника
    
    Возвращает:
    ReviewsResponse: объект с списком отзывов
    
    Исключения:
    - HTTPException: если возникла ошибка при получении отзывов
    """
    try:
        reviews = get_list_useful_reviews(worker_id)
        return {"reviews": reviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-summary", response_model=SummaryResponse)
def generate_summary_api(request: ReportRequest):
    """
    Генерирует сводку на основе отзывов о сотруднике.
    
    Аргументы:
    - request (ReportRequest): объект запроса с ID сотрудника и опциональным списком отзывов
    
    Возвращает:
    SummaryResponse: объект с текстом сводки
    
    Исключения:
    - HTTPException: если возникла ошибка при генерации сводки
    """
    reviews = request.reviews or get_list_useful_reviews(request.worker_id)
    try:
        summary = generate_summary(reviews, api)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-report", response_model=ReportResponse)
def generate_report_api(request: ReportRequest):
    """
    Создает полный отчет о сотруднике, включая оценку компетенций и навыков.
    
    Аргументы:
    - request (ReportRequest): объект запроса с ID сотрудника и опциональным списком отзывов
    
    Возвращает:
    ReportResponse: объект с оценками компетенций, списком навыков и общим баллом
    
    Исключения:
    - HTTPException: если возникла ошибка при генерации отчета
    """
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
