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
    competency: str
    score: int
    reason: str
    confirmation: str

class UsefulReport(BaseModel):
    ID_reviewer: int
    ID_under_review: int
    review: str
    review_id: int
    score: float

class WorkerDataResponse(BaseModel):
    competencies: List[Competency]
    hard_skills: List[str]
    score: float
    summary: str
    useful_reviews: List[UsefulReport]
    worker_id: int


@app.get("/worker-data/{worker_id}", response_model=WorkerDataResponse)
def get_worker_data(worker_id: int):
    """Retrieve all data for a specific worker."""
    try:
        # Retrieve all necessary information for the worker from storage
        worker_ds_path = os.getenv("WORKER_DATASET_DIR")
        with open(worker_ds_path, 'r', encoding='utf-8', errors='ignore') as file:
            worker_ds = json.load(file)

        worker_data = find_worker_by_id(worker_id, worker_ds)
        
        if not worker_data:
            raise HTTPException(status_code=404, detail="Worker data not found.")
        
        return worker_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
