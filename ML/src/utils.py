"""
Модуль утилит для обработки и извлечения отзывов о сотрудниках.
"""
import requests
import json
import ast
from dotenv import load_dotenv
import os
import re

# from .ranking_reviews import retrieve_clustered_reviews
# from .preprocessing import clean_text
from ranking_reviews import retrieve_clustered_reviews
from preprocessing import clean_text

load_dotenv()


def find_worker_by_id(worker_id, data):
    """
    Поиск данных сотрудника по его ID.

    Аргументы:
    worker_id (int): ID сотрудника
    data (list): Список данных о сотрудниках

    Возвращает:
    dict: Данные сотрудника или None, если сотрудник не найден
    """
    for worker in data:
        if worker.get("worker_id") == worker_id:
            return worker
    return None


def get_all_reviews():
    """
    Получение всех отзывов из датасета с очисткой текста отзывов.

    Возвращает:
    list: Список всех отзывов с очищенным текстом
    """
    dataset_path = os.getenv("DATASET_DIR")

    with open(dataset_path, 'r', encoding='utf-8', errors='ignore') as file:
        reviews = json.load(file)

    reviews = [
        {
            key: clean_text(value) if key == 'review' else value
            for key, value in item.items()
        }
        for item in reviews
    ]

    return reviews


def get_reviews(worker_id):
    """
    Получение отзывов для конкретного сотрудника.

    Аргументы:
    worker_id (int): ID сотрудника

    Возвращает:
    list: Список отзывов о сотруднике с очищенным текстом
    """
    dataset_path = os.getenv("DATASET_DIR")

    with open(dataset_path, 'r', encoding='utf-8', errors='ignore') as file:
        ds_reviews = json.load(file)

    reviews = [
        {
            key: clean_text(value) if isinstance(value, str) else value
            for key, value in item.items()
        }
        for item in ds_reviews
        if item['ID_under_review'] == worker_id
        and item['ID_reviewer'] != worker_id
    ]

    return reviews


def get_useful_reviews(worker_id):
    """
    Получение кластеризованных полезных отзывов о сотруднике.

    Аргументы:
    worker_id (int): ID сотрудника

    Возвращает:
    list: Список кластеризованных полезных отзывов
    """
    return retrieve_clustered_reviews(worker_id)


def get_list_useful_reviews(worker_id):
    """
    Получение списка текстов полезных отзывов о сотруднике.

    Аргументы:
    worker_id (int): ID сотрудника

    Возвращает:
    list: Список текстов полезных отзывов
    """
    reviews = get_useful_reviews(worker_id)
    return [review['review'] for review in reviews]


def extract_list(text):
    """
    Извлечение списка из текстового представления.

    Аргументы:
    text (str): Текст, содержащий представление списка

    Возвращает:
    list: Извлеченный список или исходный текст, если извлечение не удалось
    """
    try:
        match = re.search(r"\[.*?\]", text)
        if match:
            list_str = match.group(0)
            result_list = ast.literal_eval(list_str)
            if isinstance(result_list, list):
                return result_list
        return text
    except Exception as e:
        return e


def get_response(api_url, data, headers):
    """
    Отправка запроса к API и обработка ответа.

    Аргументы:
    api_url (str): URL API
    data (dict): Данные для отправки
    headers (dict): Заголовки запроса

    Возвращает:
    dict/str: Данные ответа или сообщение об ошибке
    """
    response = requests.post(api_url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        try:
            response_data = response.json()
            return response_data
        except Exception as e:
            return e
    else:
        return f"Error: {response.status_code} - {response.text}"
