"""
Модуль для генерации отчетов о сотрудниках на основе отзывов.
"""
from summary_generator import generate_summary
from competency_scoring import evaluate_competencies
from hard_skills_generator import extract_hard_skills
from self_review import analyze_self_review
from written_by_person import analyze_review_style
from utils import *
from dotenv import load_dotenv
import time
import os


load_dotenv()
api = os.getenv("API_URL")

def get_self_feedback(summary, worker_id):
    """
    Получает анализ самооценки сотрудника.

    Эта функция использует модуль self_review для анализа самооценки сотрудника
    на основе предоставленной сводки и ID сотрудника.

    Аргументы:
    summary (str): Сводка о сотруднике
    worker_id (int): ID сотрудника

    Возвращает:
    str: Анализ самооценки сотрудника
    """
    self_feedback = analyze_self_review(summary, worker_id)
    return self_feedback

def get_written_by_person(worker_id):
    """
    Получает анализ стиля написания отзывов сотрудником.

    Эта функция использует модуль written_by_person для анализа стиля и тона отзывов,
    написанных сотрудником о других сотрудниках.

    Аргументы:
    worker_id (int): ID сотрудника

    Возвращает:
    str: Анализ стиля написания отзывов сотрудником
    """
    written_by_feedback = analyze_review_style(api, worker_id)
    return written_by_feedback


def get_summary(worker_id, reviews=None):
    """
    Генерирует сводку для сотрудника на основе отзывов.

    Аргументы:
    worker_id (int): ID сотрудника
    reviews (list, optional): Список отзывов. Если не указан, будет получен автоматически.

    Возвращает:
    str: Сгенерированная сводка
    """
    if not reviews:
        reviews = get_list_useful_reviews(worker_id)

    summary = generate_summary(reviews, api)
    final_summary = summary
    final_summary += "\n\n" + get_written_by_person(worker_id)
    
    self_feedback = get_self_feedback(summary, worker_id)
    if self_feedback:
        final_summary += "\n\n" + self_feedback
    return final_summary


def get_competencies(worker_id, reviews=None):
    """
    Оценивает компетенции сотрудника на основе отзывов.

    Аргументы:
    worker_id (int): ID сотрудника
    reviews (list, optional): Список отзывов. Если не указан, будет получен автоматически.

    Возвращает:
    list: Список оцененных компетенций
    """
    if not reviews:
        reviews = get_list_useful_reviews(worker_id)
    return evaluate_competencies(reviews, api)


def get_hardskills(worker_id, reviews=None):
    """
    Выявляет технические навыки сотрудника на основе отзывов.

    Аргументы:
    worker_id (int): ID сотрудника
    reviews (list, optional): Список отзывов. Если не указан, будет получен автоматически.

    Возвращает:
    list: Список выявленных технических навыков
    """
    if not reviews:
        reviews = get_list_useful_reviews(worker_id)
    return extract_hard_skills(reviews, api)


def calculate_score(competencies):
    """
    Рассчитывает общий балл на основе оценок компетенций.

    Аргументы:
    competencies (list): Список оцененных компетенций

    Возвращает:
    float: Средний балл по всем компетенциям
    """
    total_score = 0
    for competency in competencies:
        if competency['score']:
            total_score += competency['score']
    return round(total_score / len(competencies), 2)


def get_report(worker_id, reviews=None):
    """
    Создает полный отчет о сотруднике.

    Аргументы:
    worker_id (int): ID сотрудника
    reviews (list, optional): Список отзывов. Если не указан, будет получен автоматически.

    Возвращает:
    dict: Словарь с данными отчета, включая компетенции, технические навыки и общий балл
    """
    if not reviews:
        reviews = get_list_useful_reviews(worker_id)

    competencies = get_competencies(id, reviews)
    hard_skills = get_hardskills(id, reviews)
    score = calculate_score(competencies)

    data = {
        'competencies': competencies,
        'hard_skills' : hard_skills,
        'score' : score,
    }

    return data
