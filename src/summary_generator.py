import requests
import json
from typing import List, Dict
import time


def generate_summary(reviews: List[str], api_url: str) -> str:
    """
    Генерирует краткое summary на основе списка отзывов, содержащее только полезную информацию.

    Args:
        reviews (List[str]): Список отзывов.
        api_url (str): URL для API запроса.

    Returns:
        str: Краткое summary на 1-3 предложения.
    """
    # Объединяем отзывы в один текст для запроса
    reviews_text = " ".join(reviews)

    # Подготавливаем prompt для генерации краткого summary
    prompt = f"""
    Учитывая следующие отзывы о сотруднике: "{reviews_text}", создай краткое резюме на 1-3 предложения, 
    содержащее только полезную информацию, без воды и лишних деталей.
    """
    
    # Настройка данных для API запроса
    data = {
        "prompt": [prompt],
        "apply_chat_template": True,
        "system_prompt": "Ты профессионально анализируешь отзывы и извлекаешь только важную информацию для краткого резюме.",
        "max_tokens": 150,
        "n": 1,
        "temperature": 0.2
    }

    # Выполнение запроса к API
    response = requests.post(api_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    
    # Проверка ответа и извлечение текста summary
    if response.status_code == 200:
        try:
            result = response.text
            return result
        except (KeyError, IndexError) as e:
            return e
    else:
        return "Error occured"


def get_reviews(ds_reviews, worker_id):
    return [
        item['review']
        for item in ds_reviews
        if item['ID_under_review'] == worker_id 
        # and item['ID_reviewer'] != worker_id
    ]

# Пример использования функции
api_url = "https://vk-scoreworker-case-backup.olymp.innopolis.university/generate"  # Укажите ваш API URL
# reviews = [
#     "Отлично справляется с задачами, всегда проявляет инициативу.",
#     "Хорошо работает в команде и помогает другим участникам.",
#     "Долго адаптируется к трудностям и не решает проблемы.",
#     "Четкий и структурный - это прямо про. Шарит за свое дело максимально глубоко, тут нет ни малейшего сомнения. Все задачи проходят по строгому флоу, который составлен с учетом всех нюансов проекта, которые могут возникнуть. всегда смотрит на задачу с точки зрения целей, для которых она делается, что помогает всем проектам четко понимать действительно ли они были эффективны. Зоны роста: голосом все вопросы решаются быстро и суперконструктивно, всегда можем договориться и найти наиболее компромиссное решение с точки зрения целей всех команд. В переписке сложнее найти общий язык (допускаю, что особенность во мне)",
# ]

worker_id = 6135
# ds = 'dataset\review_dataset.json'
ds = 'dataset\sample_reviews.json'

with open(ds, 'r', encoding='utf-8') as file:
    ds_reviews = json.load(file)



s = time.time()
reviews = get_reviews(ds_reviews, worker_id)
summary = generate_summary(reviews, api_url)
print(summary)
e = time.time()

print(f"\nExecution time: {e-s:.2f} sec")
