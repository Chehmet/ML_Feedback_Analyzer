"""
Модуль для оценки, кластеризации и отбора отзывов о сотрудниках.
"""
import torch
from transformers import pipeline
import random
import time
import json
import os
from sklearn.cluster import KMeans
import requests

from .preprocessing import clean_text
# from preprocessing import clean_text

# Настройка устройства для вычислений
device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)

# Критерии оценки отзывов
criteria_labels = {
    'usefulness': ['полезный', 'не полезный'],
    'content': ['содержательный', 'не содержательный'],
    'objectivity': ['объективный', 'не объективный'],
    'ethic': ['этичный', 'не этичный'],
    'honesty': ['честный', 'не честный'],
    'detail': ['подробный', 'не подробный']
}

def embedings_generator(reviews):
    """
    Генерирует эмбеддинги для списка отзывов, используя внешний API.

    Аргументы:
    reviews (list): Список текстов отзывов.

    Возвращает:
    list: Список эмбеддингов для каждого отзыва или код ошибки.
    """
    url = os.getenv("EMBEDDER_URL")
    data = {
        "inputs": reviews,
        "normalize": True,
        "truncate": False
    }
    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            embedding = response.json()
            return embedding
        else:
            print("Error:", response.status_code, response.text)
            return response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return e

def get_reviews(worker_id):
    """
    Получает и очищает отзывы для конкретного сотрудника из JSON-файла.

    Аргументы:
    worker_id (int): ID сотрудника.

    Возвращает:
    list: Список очищенных отзывов для сотрудника.
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

def evaluate_review(review):
    """
    Оценивает отзыв по заданным критериям, используя zero-shot классификацию.

    Аргументы:
    review (str): Текст отзыва.

    Возвращает:
    float: Общая оценка отзыва.
    """
    total_score = 0.0
    
    for criterion, labels in criteria_labels.items():
        result = classifier(review, labels)        
        positive_label_index = result['labels'].index(labels[0])
        positive_score = result['scores'][positive_label_index]

        if criterion == "detail":
            positive_score /= 3

        total_score += positive_score
    return total_score


def evaluate_review_of_worker(worker_id):
    """
    Оценивает все отзывы для конкретного сотрудника.

    Аргументы:
    worker_id (int): ID сотрудника.

    Возвращает:
    list: Список отзывов с добавленными оценками.
    """
    reviews = get_reviews(worker_id)
    evaluated_reviews = []
    
    for review in reviews:
        result = review
        result['score'] = evaluate_review(review['review'])
        evaluated_reviews.append(result)

    return evaluated_reviews


def retrieve_clustered_reviews(worker_id, k=15):
    """
    Кластеризует и отбирает репрезентативные отзывы для сотрудника.

    Аргументы:
    worker_id (int): ID сотрудника.
    k (int): Максимальное количество кластеров (по умолчанию 15).

    Возвращает:
    list: Список отобранных репрезентативных отзывов.
    """
    reviews = evaluate_review_of_worker(worker_id)
    useful_reviews = [review for review in reviews if review['score'] > 3.5]
    
    # Убираем короткие отзывы
    useful_reviews = [review for review in useful_reviews if len(review['review'].split()) > 15]

    review_texts = [review['review'] for review in useful_reviews]
    embeddings = embedings_generator(review_texts)

    # Кластеризация
    n_clusters = min(k, len(useful_reviews))  # Число кластеров не больше, чем количество отзывов
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(embeddings)
    
    clustered_reviews = {}
    
    for i, label in enumerate(kmeans.labels_):
        if label not in clustered_reviews:
            clustered_reviews[label] = []
        clustered_reviews[label].append(useful_reviews[i])
    
    # Выбираем один отзыв из каждого кластера
    selected_reviews = []
    for reviews in clustered_reviews.values():
        selected_reviews.append(random.choice(reviews))

    return selected_reviews
