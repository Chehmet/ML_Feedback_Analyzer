import requests
import json
import ast

def get_reviews(ds_reviews, worker_id):
    return [
        item['review']
        for item in ds_reviews
        if item['ID_under_review'] == worker_id 
        # and item['ID_reviewer'] != worker_id
    ]


def extract_list(text):
    pass

def get_response(api_url, data, headers):
    # Выполнение запроса к API
    response = requests.post(api_url, data=json.dumps(data), headers=headers)

    # Проверка статуса ответа и извлечение данных
    if response.status_code == 200:
        try:
            response_data = response.json()
            return ast.literal_eval(response_data)
        except Exception as e:
            return e
    else:
        return f"Error: {response.status_code} - {response.text}"