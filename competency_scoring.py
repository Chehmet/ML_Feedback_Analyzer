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
    prompt = f"""
    Учитывая следующие отзывы о пользователе: '{reviews_text}', 
    используя '{competencies}' определите присутствие компетенции в отзывах, и если присутствует, оцените ее по шкале от 1(очень плохо), 2(плохо), 3(нормально), 4(хорошо), 5(очень хорошо) и напишите причину КРАТКО, а также цитату из отзыва, подтверждающую вашу оценку.
    Если компетенция не присутствует в отзывах, ПРОПУСТИТЕ её.
	Ответ в формате json_object:
        "id": "<user_id>",
        "competency": "<название компетенции>",
        "score": "<оценка>",
        "reason": "<краткое описание причины>",
        "confirmation": "<цитата из отзыва>"
    """

    # Настройка данных для запроса
    data = {
        "prompt": [prompt],
        "apply_chat_template": True,
        "system_prompt": "Ты профессионально различаешь компетенции и обнаруживаешь их в обычных отзывах от сотрудников, а также выдаешь оценку на основе компетенций.",
        "max_tokens": 4096,
        "n": 1,
        "temperature": 0.4
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
    # "Отлично справляется с задачами, всегда проявляет инициативу.",
    # "Хорошо работает в команде и помогает другим участникам.",
    # "Долго адаптируется к трудностям и не решает проблемы.",
    "Четкий и структурный - это прямо про. Шарит за свое дело максимально глубоко, тут нет ни малейшего сомнения. Все задачи проходят по строгому флоу, который составлен с учетом всех нюансов проекта, которые могут возникнуть. всегда смотрит на задачу с точки зрения целей, для которых она делается, что помогает всем проектам четко понимать действительно ли они были эффективны. Зоны роста: голосом все вопросы решаются быстро и суперконструктивно, всегда можем договориться и найти наиболее компромиссное решение с точки зрения целей всех команд. В переписке сложнее найти общий язык (допускаю, что особенность во мне)",
]

user_id = 12345
competency_evaluation = evaluate_competencies(reviews, user_id, api_url)

for competency, evaluation in competency_evaluation.items():
    print(f"{competency} - Оценка: {evaluation['Оценка']}, Причинность: {evaluation['Причинность']}")
