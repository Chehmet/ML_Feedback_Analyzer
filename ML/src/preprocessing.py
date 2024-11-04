"""
Модуль для предварительной обработки и очистки текстовых отзывов.
"""
import re
import json
import time

from .utils import *
# from utils import *


def remove_non_utf8(text):
    """
    Удаляет символы, не соответствующие кодировке UTF-8.

    Аргументы:
    text (str): Исходный текст

    Возвращает:
    str: Очищенный текст, содержащий только UTF-8 символы
    """
    cleaned_text = text.encode("utf-8", "ignore").decode("utf-8")
    return cleaned_text


def clean_text(text):
    """
    Очищает текст от содержимого в квадратных скобках и лишних пробелов.

    Аргументы:
    text (str): Исходный текст

    Возвращает:
    str: Очищенный текст
    """
    cleaned_text = re.sub(r'\[.*?\]', '', text)
    return ' '.join(cleaned_text.split())


def is_relevant(review):
    """
    Определяет, является ли отзыв релевантным на основе ключевых слов и длины.

    Аргументы:
    review (str): Текст отзыва

    Возвращает:
    bool: True, если отзыв релевантный, False в противном случае
    """
    irrelevant_keywords = [
        "лучший", "классный человек", "сотрудничество",
        "молодец", "умница", "отличный", "спасибо", "рекомендую", "ужасный", "плохой"
    ]
    
    if len(review.split()) < 5:
        return False
    
    if any(keyword in review.lower() for keyword in irrelevant_keywords):
        return False

    return True


def remove_stopwords(text, stopwords):
    """
    Удаляет стоп-слова из текста.

    Аргументы:
    text (str): Исходный текст
    stopwords (set): Набор стоп-слов для удаления

    Возвращает:
    str: Текст без стоп-слов
    """
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords]
    return " ".join(filtered_words)

def preprocess_reviews(data, url):
    """
    Выполняет предварительную обработку списка отзывов.

    Эта функция применяет ряд операций очистки и фильтрации к каждому отзыву:
    - Удаление текста в квадратных скобках
    - Очистка от лишних пробелов и специальных символов
    - Удаление стоп-слов
    - Проверка релевантности отзыва

    Аргументы:
    data (list): Список исходных отзывов
    url (str): URL API (не используется в текущей версии функции)

    Возвращает:
    list: Список обработанных и отфильтрованных отзывов
    """
    stopwords = {
        "в", "на", "по", "с", "за", "для", "и", "к", "от", "о", "об", "до", "через",
        "под", "над", "у", "при", "из", "между", "а", "но", "или", "то",
        "же", "если", "как", "так", "чтобы", "ну"
    }
    processed_data = []
    cnt_b, cnt_af = 0, 0
    for entry in data:
        tokens_before = len(entry.split())
        cnt_b += tokens_before
        # Убираем текст в квадратных скобках и очищаем пробелы
        clean_text = re.sub(r"\[.*?\]", "сотрудник", entry)
        clean_text = clean_text.replace("\n", "").replace("/", "").replace("-", "").replace("  ", " ")
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        
        # Убираем стоп-слова из текста
        relevant_text = remove_stopwords(clean_text, stopwords)
        
        # Добавляем только релевантные отзывы
        if is_relevant(relevant_text):
            entry = relevant_text
            processed_data.append(entry)

        tokens_after = len(clean_text.split())
        cnt_af += tokens_after

        print(f"Tokens before: {tokens_before}\t After: {tokens_after}")
    print(f"All tokens before: {cnt_b}\t After: {cnt_af}\t Percentage: {cnt_af/cnt_b}")
    return processed_data
