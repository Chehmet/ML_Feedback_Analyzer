from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from .utils import *
from dotenv import load_dotenv
import os
import json

load_dotenv()
app = FastAPI()


class Competency(BaseModel):
    """
    Модель для представления компетенции сотрудника.

    Атрибуты:
    - competency (str): название компетенции
    - score (int): оценка компетенции
    - reason (str): обоснование оценки
    - confirmation (str): подтверждение оценки
    """
    competency: str
    score: int
    reason: str
    confirmation: str

class UsefulReport(BaseModel):
    """
    Модель для представления полезного отзыва о сотруднике.

    Атрибуты:
    - ID_reviewer (int): ID рецензента
    - ID_under_review (int): ID оцениваемого сотрудника
    - review (str): текст отзыва
    - review_id (int): уникальный ID отзыва
    - score (float): оценка, данная в отзыве
    """
    ID_reviewer: int
    ID_under_review: int
    review: str
    review_id: int
    score: float

class WorkerDataResponse(BaseModel):
    """
    Модель ответа с полными данными о сотруднике.

    Атрибуты:
    - competencies (List[Competency]): список компетенций сотрудника
    - hard_skills (List[str]): список технических навыков сотрудника
    - score (float): общий балл сотрудника
    - summary (str): краткое резюме о сотруднике
    - useful_reports (List[UsefulReport]): список полезных отзывов о сотруднике
    - worker_id (int): ID сотрудника
    """
    competencies: List[Competency]
    hard_skills: List[str]
    score: float
    summary: str
    useful_reports: List[UsefulReport]
    worker_id: int


@app.get("/worker-data/{worker_id}", response_model=WorkerDataResponse)
def get_worker_data(worker_id: int):
    """
    Получает все данные для конкретного сотрудника.

    Эта функция извлекает полную информацию о сотруднике из хранилища данных,
    включая компетенции, навыки, общий балл, резюме и полезные отзывы.

    Аргументы:
    - worker_id (int): ID сотрудника

    Возвращает:
    WorkerDataResponse: объект с полными данными о сотруднике

    Исключения:
    - HTTPException(404): если данные сотрудника не найдены
    - HTTPException(500): если произошла ошибка при обработке запроса
    """
    try:
        # Получение пути к файлу данных сотрудников из переменных окружения
        worker_ds_path = os.getenv("WORKER_DATASET_DIR")
        with open(worker_ds_path, 'r', encoding='utf-8', errors='ignore') as file:
            worker_ds = json.load(file)

        worker_data = find_worker_by_id(worker_id, worker_ds)
        
        if not worker_data:
            raise HTTPException(status_code=404, detail="Worker data not found.")
        
        return worker_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
