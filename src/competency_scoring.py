import json
from typing import List, Dict
import time
from .utils import *
import ast


# Определение компетенций
competencies = [
    "Профессионализм",
    "Инициативность",
    "Умение решать конфликты",
    "Лидерство",
    "Таймменеджмент",
    "Адаптивность",
    "Ответственность",
    "Целеустремленность",
    "Саморазвитие",
    "Коммуникация"
]


def evaluate_competencies(reviews: List[str], api_url: str) -> Dict[str, Dict[str, str]]:
    """
    Оценивает компетенции по отзывам и возвращает оценки и объяснения.

    Args:
        reviews (List[str]): Список отзывов для пользователя.
        worker_id (int): ID пользователя.
        api_url (str): URL для API запроса.

    Returns:
        Dict[str, Dict[str, str]]: Оценки и объяснения для каждой компетенции.
    """
    # Объединяем отзывы в один текст для запроса
    reviews_text = " ".join(reviews)

    # Формируем запрос к модели для каждой компетенции
    prompt = f"""
    Учитывая следующие отзывы о пользователе: '{reviews_text}', 
    используя '{competencies}' определите присутствие компетенции 
    в отзывах, и если присутствует, оцените ее по шкале от 1(очень плохо),
    2(плохо), 3(нормально), 4(хорошо), 5(очень хорошо) и напишите причину 
    КРАТКО, а также цитату из отзыва, подтверждающую вашу оценку.
    Если компетенция не присутствует в отзывах, ПРОПУСТИТЕ её.
	Ответ в формате json_object:
        "competency": "<название компетенции>",
        "score": "<оценка>",
        "reason": "<краткое описание причины>",
        "confirmation": "<цитата из отзыва>"
    """

    # Настройка данных для запроса
    data = {
        "prompt": [prompt],
        "apply_chat_template": True,
        "system_prompt": "Ты профессионально различаешь компетенции и обнаруживаешь их в обычных отзывах от сотрудников, а также выдаешь оценку на основе компетенций.",
        "max_tokens": 4096,
        "n": 1,
        "temperature": 0.2,
        # "top_k": 15,
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    response = get_response(api_url, data, headers)
    return ast.literal_eval(response)


# Пример использования функции

# api_url = "https://vk-scoreworker-case.olymp.innopolis.university/generate"
# # api_url = "https://vk-scoreworker-case-backup.olymp.innopolis.university/generate"

# worker_id = 6135


# s = time.time()
# reviews = get_reviews(worker_id)
# competency_evaluation = evaluate_competencies(reviews, api_url)
# print(competency_evaluation)
# e = time.time()

# print(f"\nExecution time: {e-s:.2f} sec")
