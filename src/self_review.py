# Here we have information about how person writes reviews to others,
# if all of them are negative, or all of them are too positive
import requests
import json
import time
# from utils import *

def get_self_reviews(ds_reviews, worker_id):
    return [
        item['review']
        for item in ds_reviews
        if item['ID_under_review'] == worker_id
    ]


def analyze_review_style(api_url, self_rewiews, summary, worker_id) -> str:
    self_reviews = " ".join(self_rewiews)
    
    # Construct the prompt to analyze the tone of reviews
    prompt = f"""
    Проанализируй отзывы, написанные сотрудником: {self_reviews} и описание сотрудника: {summary}. 
    Сравни описание сотрудника и как он оценивает себя. Оцени самооценку сотрудника.    
    Ответ должен быть в виде 1-2 коротких предложений, также добавь небольшую рекомендацию по поддержке сотрудника, если нужно.
    Не используй '\n' и другие знаки в ответе, пиши в формате длинной строки.
    """

    # Set up the data for API request
    data = {
        "prompt": [prompt],
        "apply_chat_template": True,
        "system_prompt": "Ты опытный психолог, который анализирует самооценку сотрудника. ",
        "max_tokens": 200,
        "n": 1,
        "temperature": 0.2
    }

    headers = {
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.post(api_url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        error_message = f"Error: {response.status_code} - {response.text}"
        print(error_message)
        return error_message

# Example usage of the function
api_url = "https://vk-scoreworker-case.olymp.innopolis.university/generate"  # Replace with actual API URL
worker_id = 28
# ds = r'dataset\review_dataset.json'
ds = '../dataset/sample_reviews.json'

with open(ds, 'r', encoding='utf-8') as file:
    ds_reviews = json.load(file)

s = time.time()
self_reviews = get_self_reviews(ds_reviews, worker_id)
summary = (
    "Сотрудник открыт к диалогу, проявляет профессионализм и нацелен на результат. "
    "Вежлив, в общении конструктивен, всегда готов объяснить свои решения. "
    "Однако иногда демонстрирует склонность к излишней осторожности."
)

writer_style = analyze_review_style(api_url, self_reviews, summary, worker_id)
print(writer_style)
e = time.time()
print(f"\nExecution time: {e-s:.2f} sec")
