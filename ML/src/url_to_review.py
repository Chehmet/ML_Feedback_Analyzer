import hashlib
import json
import os
from utils import *
from competency_scoring import *
from preprocessing import clean_text
from dotenv import load_dotenv


def hash_func(review_text, reviewer_id):
    """
    Генерирует уникальный хеш для каждого отзыва, используя текст отзыва и ID рецензента.

    Аргументы:
        review_text (str): Текст отзыва.
        reviewer_id (int): ID рецензента.

    Возвращает:
        str: Уникальная хеш-строка для отзыва.
    """
    unique_string = f"{reviewer_id}_{review_text}"
    # Create hash using SHA-256
    review_hash = hashlib.sha256(unique_string.encode()).hexdigest()
    # Convert the first 8 characters of the hash to an integer and then to a decimal string
    decimal_id = int(review_hash[:8], 16)
    return decimal_id


def add_unique_ids_to_reviews(db):
    """
    Добавляет уникальный ID отзыва к каждому отзыву в наборе данных.

    Аргументы:
        db (list): Список отзывов, где каждый отзыв представлен словарем.

    Возвращает:
        list: Обновленный список отзывов с добавленными уникальными ID.
    """
    for review in db:
        review_id = hash_func(review['review'], review['ID_reviewer'])
        review['review_id'] = review_id
    return db


def url_review(citate, db):
    """
    Находит уникальный ID отзыва, содержащего данную цитату.

    Аргументы:
        citate (str): Цитата или выдержка для поиска.
        db (list): Список отзывов, где каждый отзыв представлен словарем.

    Возвращает:
        str: Уникальный хеш-ID отзыва, содержащего цитату, или None, если не найдено."""
    for review in db:
        if citate.lower() in review['review'].lower():
            if 'review_id' in review and review['review_id']:
                return review["review_id"]
            else: # Generate and return the hash for the matching review
                return hash_func(review['review'], review['ID_reviewer'])


def save_to_json(data, filepath):
    """
    Сохраняет обработанные данные в JSON-файл.

    Аргументы:
        data (list): Список обработанных отзывов с уникальными ID.
        filepath (str): Путь для сохранения JSON-файла.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    # Write the data to JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_competency_references(worker_id):
    """
    Получает оценки компетенций сотрудника с ссылками на соответствующие отзывы.

    Эта функция выполняет следующие шаги:
    1. Получает список полезных отзывов для указанного сотрудника.
    2. Оценивает компетенции на основе этих отзывов.
    3. Для каждой оценки компетенции находит соответствующий ID отзыва.

    Аргументы:
        worker_id (int): Уникальный идентификатор сотрудника.

    Возвращает:
        list: Список словарей, каждый из которых содержит оценку компетенции
        и ссылку на соответствующий отзыв
    """
    db = get_all_reviews()
    reviews = get_list_useful_reviews(worker_id)
    url = os.getenv("API_URL")
    competency_evaluation = evaluate_competencies(reviews, url)
    for i in range(len(competency_evaluation)):
        citate = competency_evaluation[i]["confirmation"]
        review_id = url_review(citate, db)
        competency_evaluation[i]['ref'] = review_id
    return competency_evaluation


load_dotenv()

# Вызов функции, чтобы делать айди для каждого ревью
# db_with_ids = add_unique_ids_to_reviews(db)
# save_to_json(db_with_ids, r'dataset\new_dataset.json')
# cnt = 0
# for review in db_with_ids:
#     cnt += 1
#     if cnt <= 5:
#         print(review)
