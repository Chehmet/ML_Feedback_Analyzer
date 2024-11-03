import json
from typing import List, Dict
import time

from .utils import *
# from utils import *


def generate_summary(reviews: List[str], api_url: str) -> str:
    """
    Генерирует краткое summary на основе списка отзывов, содержащее только полезную информацию.

    Args:
        reviews (List[str]): Список отзывов.
        api_url (str): URL для API запроса.

    Returns:
        str: Краткое summary на 1-3 предложения.
    """
    # Объединяем отзывы в один текст для запроса
    reviews_text = " ".join(reviews)

    # Подготавливаем prompt для генерации краткого summary
    prompt = f"""
    Учитывая следующие отзывы о сотруднике: "{reviews_text}", создай краткое резюме на 1-3 предложения, 
    содержащее только полезную информацию, без воды и лишних деталей.
    """
    
    # Настройка данных для API запроса
    data = {
        "prompt": [prompt],
        "apply_chat_template": True,
        "system_prompt": "Ты профессионально анализируешь отзывы и извлекаешь только важную информацию для краткого резюме.",
        "max_tokens": 200,
        "n": 1,
        # "top_k": 15,
        "temperature": 0.2,
    }

    headers = {
        "Content-Type": "application/json"
    }

    return get_response(api_url, data, headers)


# Пример использования функции

# api_url = "https://vk-scoreworker-case.olymp.innopolis.university/generate"

# worker_id = 6135


# s = time.time()
# reviews = get_reviews(worker_id)
# summary = generate_summary(reviews, api_url)
# print(summary)
# e = time.time()

# print(f"\nExecution time: {e-s:.2f} sec")
