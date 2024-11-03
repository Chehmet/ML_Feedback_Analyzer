import requests
import json
import ast
from dotenv import load_dotenv
import os
import re
from ranking_reviews import retrieve_clustered_reviews

load_dotenv()


def get_reviews(worker_id):
    dataset_path = os.getenv("DATASET_DIR")

    with open(dataset_path, 'r', encoding='utf-8') as file:
        ds_reviews = json.load(file)

    return [
        item['review']
        for item in ds_reviews
        if item['ID_under_review'] == worker_id
        and item['ID_reviewer'] != worker_id
    ]


def get_useful_reviews(worker_id):
    return retrieve_clustered_reviews(worker_id)


def get_list_useful_reviews(worker_id):
    reviews = get_useful_reviews(worker_id)
    return [review['review'] for review in reviews]


def extract_list(text):
    try:
        match = re.search(r"\[.*?\]", text)
        if match:
            list_str = match.group(0)
            result_list = ast.literal_eval(list_str)
            if isinstance(result_list, list):
                return result_list
        return text
    except Exception as e:
        return e


def get_response(api_url, data, headers):
    # Выполнение запроса к API
    response = requests.post(api_url, data=json.dumps(data), headers=headers)

    # Проверка статуса ответа и извлечение данных
    if response.status_code == 200:
        try:
            response_data = response.json()
            return response_data
        except Exception as e:
            return e
    else:
        return f"Error: {response.status_code} - {response.text}"
