import hashlib
import json
import os
from utils import *
from competency_scoring import *
from preprocessing import clean_text


def hash_func(review_text, reviewer_id):
    """
    Generates a unique hash for each review using the review text and reviewer ID.
    
    Args:
        review_text (str): The text of the review.
        reviewer_id (int): The ID of the reviewer.
        
    Returns:
        str: Unique hash string for the review.
    """
    unique_string = f"{reviewer_id}_{review_text}"
    # Create hash using SHA-256
    review_hash = hashlib.sha256(unique_string.encode()).hexdigest()
    # Convert the first 8 characters of the hash to an integer and then to a decimal string
    decimal_id = int(review_hash[:8], 16)
    return decimal_id


def add_unique_ids_to_reviews(db):
    """
    Adds a unique review ID to each review in the dataset.
    
    Args:
        db (list): List of reviews, where each review is a dictionary.
        
    Returns:
        list: Updated list of reviews with unique IDs added.
    """
    for review in db:
        review_id = hash_func(review['review'], review['ID_reviewer'])
        review['review_id'] = review_id
    return db


def url_review(citate, db):
    """
    Finds the unique ID of the review containing the given citation.
    
    Args:
        citate (str): The quote or citation to search for.
        db (list): List of reviews, where each review is a dictionary.
        
    Returns:
        str: Unique hash ID of the review containing the citation, or None if not found.
    """
    for review in db:
        # print(citate.lower())
        if citate.lower() in review['review'].lower():
            if 'review_id' in review and review['review_id']:
                return review["review_id"]
            else: # Generate and return the hash for the matching review
                return hash_func(review['review'], review['ID_reviewer'])


def save_to_json(data, filepath):
    """
    Saves the processed data to a JSON file.
    
    Args:
        data (list): List of processed reviews with unique IDs.
        filepath (str): Path to save the JSON file.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    # Write the data to JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = get_all_reviews()[:100]

# Вызов функции, чтобы делать айди для каждого ревью
# db_with_ids = add_unique_ids_to_reviews(db)
# save_to_json(db_with_ids, r'dataset\new_dataset.json')
# cnt = 0
# for review in db_with_ids:
#     cnt += 1
#     if cnt <= 5:
#         print(review)

api_url = "https://vk-scoreworker-case.olymp.innopolis.university/generate"
worker_id = 105560
print("___________________")
reviews = get_list_useful_reviews(worker_id)
print("___________________")
competency_evaluation = evaluate_competencies(reviews, api_url)
print("___________________")
print(competency_evaluation)

for i in competency_evaluation:
    citate = i["confirmation"]
    review_id = url_review(citate, db)
    print(review_id, citate)
    print(citate.lower())

# citate = "Оперативно, понятно, просто и без лишней боли"
# review_id = url_review(citate, db)
# print("Review ID for citation:", review_id)

# # Generate and print all review IDs in the dataset
# for review in db:
#     review_id = hash_func(review['review'], review['ID_reviewer'])
#     print(f"Review Hash ID for reviewer {review['ID_reviewer']}: {review_id}")