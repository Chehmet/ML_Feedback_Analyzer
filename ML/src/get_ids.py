from utils import *

ds = get_all_reviews()
worker_ids = set()

for item in ds:
    worker_ids.add(item['ID_under_review'])

print(len(worker_ids))