import re
import json
import time
from utils import *


def is_relevant(review):
    # Определение ключевых слов и критериев для нерелевантных отзывов
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
    # Убираем все стоп-слова из текста
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords]
    return " ".join(filtered_words)

def preprocess_reviews(data, url):
    # Определяем список стоп-слов (предлоги, союзы и прочие)
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



ds = r'dataset\review_dataset.json'

with open(ds, 'r', encoding='utf-8') as file:
    ds_reviews = json.load(file)
    # print(ds_reviews)
# all_reviews = [item["review"] for item in ds_reviews]

worker_id = 6135
api_url = "https://vk-scoreworker-case-backup.olymp.innopolis.university/generate"  # Укажите ваш API URL

s = time.time()
reviews = get_reviews(ds_reviews, worker_id)
preprocessed = preprocess_reviews(reviews, api_url)
print(preprocessed)
e = time.time()

print(f"\nExecution time: {e-s:.2f} sec")