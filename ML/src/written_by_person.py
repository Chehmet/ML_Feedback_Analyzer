"""
Модуль для анализа стиля написания отзывов сотрудником.
"""
import requests
import json
import time
from utils import *


def get_reviews_written_by_person(worker_id):
    """
    Извлекает отзывы, написанные конкретным сотрудником о других сотрудниках.

    Эта функция использует вспомогательную функцию get_all_reviews() из модуля utils
    для получения всех отзывов, а затем фильтрует их, оставляя только те, которые
    написаны указанным сотрудником о других сотрудниках.

    Аргументы:
    worker_id (int): ID сотрудника, чьи отзывы нужно извлечь

    Возвращает:
    list: Список отзывов, написанных указанным сотрудником
    """
    ds_reviews = get_all_reviews()

    return [
        item['review']
        for item in ds_reviews
        if item['ID_reviewer'] == worker_id and not item['ID_under_review'] == worker_id
    ]

def analyze_review_style(api_url, worker_id) -> str:
    """
    Анализирует стиль и тон отзывов, написанных сотрудником.

    Эта функция:
    1. Получает отзывы, написанные сотрудником, используя get_reviews_written_by_person
    2. Объединяет все отзывы в единый текст
    3. Формирует запрос к API для анализа тона и стиля отзывов
    4. Отправляет запрос и обрабатывает ответ

    Функция определяет, являются ли отзывы преимущественно положительными, 
    отрицательными или сбалансированными.

    Аргументы:
    api_url (str): URL API для обработки текста
    worker_id (int): ID сотрудника

    Возвращает:
    str: Анализ стиля написания отзывов сотрудником или сообщение об ошибке
    """
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
        "max_tokens": 4096,
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
