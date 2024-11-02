import requests
import json
from typing import List, Dict
import time

# Определение компетенций
competencies = [
    "Профессионализм",
    "Инициативность",
    "Работа в команде",
    "Лидерство",
    "Планирование",
    "Адаптивность",
    "Решительность",
    "Ответственность",
    "Целеустремленность",
    "Саморазвитие",
    "Коммуникация"
]

def evaluate_competencies(reviews: List[str], worker_id: int, api_url: str) -> Dict[str, Dict[str, str]]:
    """
    Оценивает компетенции по отзывам и возвращает оценки и объяснения.

    Args:
        reviews (List[str]): Список отзывов для пользователя.
        user_id (int): ID пользователя.
        api_url (str): URL для API запроса.

    Returns:
        Dict[str, Dict[str, str]]: Оценки и объяснения для каждой компетенции.
    """
    # Объединяем отзывы в один текст для запроса
    reviews_text = " ".join(reviews)
    results = {}

    # Формируем запрос к модели для каждой компетенции
    for competency in competencies:
        prompt = f"""
        Учитывая следующие отзывы о пользователе {worker_id}: "{reviews_text}", 
        оцените компетенцию '{competency}' по шкале от 1 до 5 и кратко объясните оценку.
        Ответ в формате:
        Оценка: <оценка>
        Причинность: <объяснение>
        """

        # Настройка данных для запроса
        data = {
            "prompt": [prompt],
            "apply_chat_template": True,
            "system_prompt": "",
            "max_tokens": 4096,
            "n": 1,
            "temperature": 0.7
        }
        
        headers = {
            "Content-Type": "application/json"
        }

        # Выполнение запроса к API
        response = requests.post(api_url, data=json.dumps(data), headers=headers)

        # Проверка статуса ответа и извлечение данных
        if response.status_code == 200:
            try:
                response_data = response.json()
                print(response_data)
                # Извлечение оценки и объяснения из ответа
                # output_text = response_data['choices'][0]['text'].strip().split("\n")
                # rating = next((line.split(":")[1].strip() for line in output_text if line.startswith("Оценка")), "N/A")
                # reason = next((line.split(":")[1].strip() for line in output_text if line.startswith("Причинность")), "N/A")
                
                # results[competency] = {
                #     "Оценка": rating,
                #     "Причинность": reason
                # }
            except (KeyError, IndexError) as e:
                results[competency] = {
                    "Оценка": "Ошибка",
                    "Причинность": f"Ошибка извлечения данных: {e}"
                }
        else:
            results[competency] = {
                "Оценка": "Ошибка",
                "Причинность": f"Ошибка: {response.status_code} - {response.text}"
            }

    return results


def extract_hard_skills(reviews: List[str], worker_id: int, api_url: str) -> Dict[str, Dict[str, str]]:
    # Объединяем отзывы в один текст для запроса
    reviews_text = " ".join(reviews)
    results = {}

    prompt = f"""
        Учитывая следующие отзывы о сотруднике {worker_id}: "{reviews_text}", 
        выяви его hard скиллы, если они описаны в отзывах. Верни только
        питоновский список hard скиллов. Будь краток и содержателен.
        Hard скилы не должны включать мягкие навыки! Верни пустой список,
        если хард скилы не описаны в отзывах.
        """
    
    # Настройка данных для запроса
    data = {
        "prompt": [prompt],
        "apply_chat_template": False,  # True
        "system_prompt": "",
        "max_tokens": 4096,
        "n": 1,
        "temperature": 0.3  # поменять?
    }
        
    headers = {
        "Content-Type": "application/json"
    }

    # Выполнение запроса к API
    response = requests.post(api_url, data=json.dumps(data), headers=headers)

    # Проверка статуса ответа и извлечение данных
    if response.status_code == 200:
        try:
            response_data = response.json()
            print(response_data)
        except (KeyError, IndexError) as e:
            return e
    else:
        return "Error occured"

    return results


def get_reviews(ds_reviews, worker_id):
    return [
        item['review']
        for item in ds_reviews
        if item['ID_under_review'] == worker_id 
        # and item['ID_reviewer'] != worker_id
    ]


# Пример использования функции
api_url = "https://vk-scoreworker-case-backup.olymp.innopolis.university/generate"  # Укажите ваш API URL

# Пример
# user_id = 12345
# reviews = [
#     "Отлично справляется с задачами, всегда проявляет инициативу.",
#     "Хорошо работает в команде и помогает другим участникам.",
#     "Быстро адаптируется к новым условиям и решает проблемы.",
#     "Долго адаптируется к трудностям и не решает проблемы."
# ]

worker_id = 6135

# ds = 'dataset\review_dataset.json'
ds = 'dataset\sample_reviews.json'
with open(ds, 'r', encoding='utf-8') as file:
    ds_reviews = json.load(file)


s = time.time()
reviews = get_reviews(ds_reviews, worker_id)
print(reviews)

hard_skills = extract_hard_skills(reviews, worker_id, api_url)
e = time.time()

print(f"Execution time: {e-s}")

