"""
Модуль для анализа стиля написания отзывов сотрудником.
"""
import requests
import json
import time
# from utils import *
import os
from dotenv import load_dotenv

def get_reviews_written_by_person(ds_reviews, worker_id):
    """
    Извлекает отзывы, написанные конкретным сотрудником о других сотрудниках.

    Аргументы:
    ds_reviews (list): Список всех отзывов
    worker_id (int): ID сотрудника, чьи отзывы нужно извлечь

    Возвращает:
    list: Список отзывов, написанных указанным сотрудником
    """
    return [
        item['review']
        for item in ds_reviews
        if item['ID_reviewer'] == worker_id and not item['ID_under_review'] == worker_id
    ]

def analyze_review_style(api_url, reviews, worker_id) -> str:
    """
    Анализирует стиль и тон отзывов, написанных сотрудником.

    Эта функция отправляет запрос к API для анализа тона и стиля отзывов.
    Она определяет, являются ли отзывы преимущественно положительными, 
    отрицательными или сбалансированными.

    Аргументы:
    api_url (str): URL API для обработки текста
    reviews (list): Список отзывов для анализа
    worker_id (int): ID сотрудника (не используется в текущей реализации)

    Возвращает:
    str: Анализ стиля написания отзывов сотрудником
    """
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

load_dotenv()
api_url = os.getenv("API_URL")
# worker_id = 28
# ds = r'dataset\review_dataset.json'
# # ds = '../dataset/sample_reviews.json'

# with open(ds, 'r', encoding='utf-8') as file:
#     ds_reviews = json.load(file)

# s = time.time()
# reviews = get_reviews_written_by_person(ds_reviews, worker_id)

# writer_style = analyze_review_style(api_url, reviews, worker_id)

# print(writer_style)
# e = time.time()
# print(f"\nExecution time: {e-s:.2f} sec")
