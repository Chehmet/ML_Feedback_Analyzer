import json


with open('review_dataset.json', 'r', encoding='utf-8') as file:
    reviews = json.load(file)

# print(type(reviews))


# Step 1: Detect instances where a reviewer reviewed themselves
self_reviews = [review for review in reviews if review["ID_reviewer"] == review["ID_under_review"]]

# Step 2: Create sets of reviewer and worker IDs
reviewer_ids = {review["ID_reviewer"] for review in reviews}
worker_ids = {review["ID_under_review"] for review in reviews}

# Step 3: Find the intersection of reviewer and worker IDs
intersection_ids = reviewer_ids.intersection(worker_ids)

# Output the results
print("Self-reviews detected:")
for review in self_reviews:
    print(f"Reviewer ID: {review['ID_reviewer']} reviewed themselves with Review: {review['review']}")

# print("\nReviewer IDs:", reviewer_ids)
# print("Worker IDs:", worker_ids)
print("Number of Self-reviewed:", len(self_reviews))
print("Intersection of Reviewer and Worker IDs:", intersection_ids)
