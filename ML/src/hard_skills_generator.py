"""
Модуль для извлечения технических навыков (hard skills) из отзывов о сотрудниках.
"""
import json
from typing import List, Dict
import time

# from .utils import *
from utils import *


def extract_hard_skills(reviews: List[str], api_url: str) -> List[str]:
    """
    Извлекает технические навыки (hard skills) из списка отзывов о сотруднике.

    Эта функция выполняет следующие шаги:
    1. Объединяет все отзывы в единый текст.
    2. Формирует запрос к языковой модели для анализа текста и выделения технических навыков.
    3. Отправляет запрос к API языковой модели.
    4. Обрабатывает ответ и извлекает список навыков.

    Аргументы:
    reviews (List[str]): Список строк, содержащих отзывы о сотруднике.
    api_url (str): URL-адрес API языковой модели.

    Возвращает:
    List[str]: Список выявленных технических навыков. Если навыки не обнаружены,
               возвращается пустой список.
    """
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
        "temperature": 0.2,
        # "top_k": 15,
    }
        
    headers = {
        "Content-Type": "application/json"
    }

    response = get_response(api_url, data, headers)
    return extract_list(response)