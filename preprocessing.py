import re
import json


def preprocess_reviews(data):
    processed_data = []
    for entry in data:
        # Remove text within square brackets, including brackets themselves
        clean_text = re.sub(r"\[.*?\]", "", entry["review"])
        # Replace "\n" and "\n\n" with a single space
        clean_text = clean_text.replace("\n", " ").replace("  ", " ")
        clean_text = re.sub(r"\s+", " ", clean_text)
        entry["review"] = clean_text.strip()
        processed_data.append(entry)
    return processed_data


""" Example of Usage"""

# # Load the data from the input JSON file
# with open("../dataset/review_dataset.json", 'r', encoding='utf-8') as file:
#     data = json.load(file)

# processed_data = preprocess_reviews(data)

# with open('../dataset/preprocessed_review_dataset.json', 'w', encoding='utf-8') as file:
#     json.dump(processed_data, file, indent=2, ensure_ascii=False)

# print("Preprocessed data has been saved to preprocessed_review_dataset.json.")