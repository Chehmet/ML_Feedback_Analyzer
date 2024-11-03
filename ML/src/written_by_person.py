"""
Модуль для анализа стиля написания отзывов сотрудником.
"""
import requests
import json
import time
from utils import *


def get_reviews_written_by_person(worker_id):
    ds_reviews = get_all_reviews()

    return [
        item['review']
        for item in ds_reviews
        if item['ID_reviewer'] == worker_id and not item['ID_under_review'] == worker_id
    ]

def analyze_review_style(api_url, worker_id) -> str:
    reviews = get_reviews_written_by_person(worker_id)
    reviews_text = " ".join(reviews)
    
    prompt = f"""
    Пронализируй следующие отзывы: "{reviews_text}". 
    Определи, имеют ли они в основном положительный, отрицательный или сбалансированный тон. 
    Укажи, склонен ли этот пользователь оставлять чрезмерно положительные отзывы, чрезмерно критичные, 
    либо сбалансированные, с оценкой качества работы других.
    Ответ кратко в формате в виде связного отдельного короткого параграфа 1-2 предложения:
    Начни так: "Отзывы сотдрудника ..."
    Не используй '\n' и другие знаки в ответе.
    """

    data = {
        "prompt": [prompt],
        "apply_chat_template": True,
        "system_prompt": "Ты опытный психолог.",
        "max_tokens": 150,
        "n": 1,
        "temperature": 0.2
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        error_message = f"Error: {response.status_code} - {response.text}"
        print(error_message)
        return error_message
