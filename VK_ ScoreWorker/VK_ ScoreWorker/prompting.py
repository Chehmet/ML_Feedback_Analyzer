import requests
import json
from typing import List, Dict

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

def evaluate_competencies(reviews: List[str], user_id: int, api_url: str) -> Dict[str, Dict[str, str]]:
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
        Учитывая следующие отзывы о пользователе {user_id}: "{reviews_text}", 
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

# Пример использования функции
api_url = "https://vk-scoreworker-case-backup.olymp.innopolis.university/generate"  # Укажите ваш API URL
reviews = [
    "Отлично справляется с задачами, всегда проявляет инициативу.",
    "Хорошо работает в команде и помогает другим участникам.",
    "Быстро адаптируется к новым условиям и решает проблемы.",
    "Долго адаптируется к трудностям и не решает проблемы."
]

user_id = 12345
competency_evaluation = evaluate_competencies(reviews, user_id, api_url)

for competency, evaluation in competency_evaluation.items():
    print(f"{competency} - Оценка: {evaluation['Оценка']}, Причинность: {evaluation['Причинность']}")
