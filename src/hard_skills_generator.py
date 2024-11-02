import json
from typing import List, Dict
import time
from utils import *


def extract_hard_skills(reviews: List[str], api_url: str) -> List[str]:
    # Объединяем отзывы в один текст для запроса
    reviews_text = " ".join(reviews)

    prompt = f"""
        Учитывая следующие отзывы о сотруднике: "{reviews_text}", 
        выяви его hard скиллы, если они описаны в отзывах. Верни только
        питоновский список hard скиллов. Будь краток и содержателен.
        Hard скилы не должны включать мягкие навыки! Верни пустой список,
        если хард скилы не описаны в отзывах.
        """
    
    # Настройка данных для запроса
    data = {
        "prompt": [prompt],
        "apply_chat_template": False,  # True
        "system_prompt": "Ты профессионально анализируешь отзывы и извлекаешь только важную информацию о ключевых навыках сотрудника.",
        "max_tokens": 100,
        "n": 1,
        "temperature": 0.2
    }
        
    headers = {
        "Content-Type": "application/json"
    }

    return get_response(api_url, data, headers, data_structure=True)


# Пример использования функции
api_url = "https://vk-scoreworker-case-backup.olymp.innopolis.university/generate"  # Укажите ваш API URL

worker_id = 6135
# ds = 'dataset\review_dataset.json'
ds = 'dataset\sample_reviews.json'

with open(ds, 'r', encoding='utf-8') as file:
    ds_reviews = json.load(file)


s = time.time()
reviews = get_reviews(ds_reviews, worker_id)
hard_skills = extract_hard_skills(reviews, api_url)
print(hard_skills)
e = time.time()

print(f"Execution time: {e-s:.2f} sec")

