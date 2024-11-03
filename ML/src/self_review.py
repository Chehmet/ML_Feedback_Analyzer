"""
Модуль для анализа тона и стиля написания отзывов сотрудником и оценки его самооценки.
"""
import requests
import json
import time
# from utils import *
from dotenv import load_dotenv
import os

def get_self_reviews(ds_reviews, worker_id):
    """
    Извлекает отзывы, написанные конкретным сотрудником.

    Аргументы:
    ds_reviews (list): Список всех отзывов
    worker_id (int): ID сотрудника

    Возвращает:
    list: Список отзывов, написанных сотрудником
    """
    return [
        item['review']
        for item in ds_reviews
        if item['ID_under_review'] == worker_id
    ]


def analyze_review_style(api_url, self_rewiews, summary, worker_id) -> str:
    """
    Анализирует стиль написания отзывов сотрудника и его самооценку.

    Эта функция отправляет запрос к API для анализа отзывов, написанных сотрудником,
    и сравнивает их с общим описанием сотрудника. Результат включает оценку самооценки
    и возможные рекомендации по поддержке сотрудника.

    Аргументы:
    api_url (str): URL API для обработки текста
    self_reviews (list): Список отзывов, написанных сотрудником
    summary (str): Общее описание сотрудника
    worker_id (int): ID сотрудника (не используется в текущей реализации)

    Возвращает:
    str: Анализ стиля написания отзывов и самооценки сотрудника
    """
    self_reviews = " ".join(self_rewiews)
    
    prompt = f"""
    Проанализируй отзывы, написанные сотрудником: {self_reviews} и описание сотрудника: {summary}. 
    Сравни описание сотрудника и как он оценивает себя. Оцени самооценку сотрудника.    
    Ответ должен быть в виде 1-2 коротких предложений, также добавь небольшую рекомендацию по поддержке сотрудника, если нужно.
    Не используй '\n' и другие знаки в ответе, пиши в формате длинной строки.
    """
    data = {
        "prompt": [prompt],
        "apply_chat_template": True,
        "system_prompt": "Ты опытный психолог, который анализирует самооценку сотрудника. ",
        "max_tokens": 200,
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
worker_id = 28
# ds = r'dataset\review_dataset.json'
ds = '../dataset/sample_reviews.json'

with open(ds, 'r', encoding='utf-8') as file:
    ds_reviews = json.load(file)

s = time.time()
self_reviews = get_self_reviews(ds_reviews, worker_id)
summary = (
    "Сотрудник открыт к диалогу, проявляет профессионализм и нацелен на результат. "
    "Вежлив, в общении конструктивен, всегда готов объяснить свои решения. "
    "Однако иногда демонстрирует склонность к излишней осторожности."
)

writer_style = analyze_review_style(api_url, self_reviews, summary, worker_id)
print(writer_style)
e = time.time()
print(f"\nExecution time: {e-s:.2f} sec")
