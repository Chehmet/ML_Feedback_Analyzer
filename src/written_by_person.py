# Here we have information about how person writes reviews to others,
# if all of them are negative, or all of them are too positive
import requests
import json
import time
from utils import *


def get_my_reviews(ds_reviews, worker_id):
    return [
        item['review']
        for item in ds_reviews
        if item['ID_reviewer'] == worker_id 
    ]


def analyze_review_style(api_url, reviews, worker_id):
    reviews_text = " ".join(reviews)
    
    # Construct the prompt to analyze the tone of reviews
    prompt = f"""
    Анализируй следующие отзывы, написанные пользователем с ID {worker_id}: "{reviews_text}". 
    Определи, имеют ли они в основном положительный, отрицательный или сбалансированный тон. 
    Укажи, склонен ли этот пользователь оставлять чрезмерно положительные отзывы, чрезмерно критичные, 
    либо сбалансированные, с оценкой качества работы других.
    Ответ в формате:
    Тон: <оценка>
    Объяснение: <причина>
    """

    # Set up the data for API request
    data = {
        "prompt": [prompt],
        "apply_chat_template": True,
        "system_prompt": "Ты профессионально различаешь тональность отзывов, анализируя, положительны ли, отрицательны или сбалансированы они.",
        "max_tokens": 150,
        "n": 1,
        "temperature": 0.2
    }

    headers = {
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    print(response.text)
    # Process the response and return analysis
    # if response.status_code == 200:
        # result = response.json()['choices'][0]['text'].strip()
        # print("Review Style Analysis:", result)
        # return result
    # else:
    #     error_message = f"Error: {response.status_code} - {response.text}"
    #     print(error_message)
    #     return error_message

# Example usage of the function
api_url = "https://vk-scoreworker-case.olymp.innopolis.university/generate"  # Replace with actual API URL
worker_id = 28
ds = r'dataset\review_dataset.json'

with open(ds, 'r', encoding='utf-8') as file:
    ds_reviews = json.load(file)

s = time.time()
reviews = get_my_reviews(ds_reviews, worker_id)
writer_style = analyze_review_style(api_url, reviews, worker_id)
print(writer_style)
e = time.time()
print(f"\nExecution time: {e-s:.2f} sec")

