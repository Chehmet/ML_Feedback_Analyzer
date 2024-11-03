from report_generator import *
from utils import *
import json
import time


dataset = get_all_reviews()

worker_id_set = {56325, 25098, 6159, 6164, 26142, 17439, 31, 37413, 6185, 18480, 113201, 32305, 6196, 52276, 24125, 1091, 42056, 11854, 21582, 4179, 20565, 13398, 105560, 25692, 16991, 6247, 11369, 37999, 23153, 10355} # store all the worker_ids from dataset
# worker_id_set = {113201}

# workers_info = [None for _ in range(len(worker_id_set))]

with open(r"ml\dataset\workers_info.json", "r", encoding="utf-8") as file:
    workers_info = json.load(file)

s = time.time()
for id in worker_id_set:
    useful_reviews = get_useful_reviews(id)
    list_useful_reviews = [review['review'] for review in useful_reviews]
    report = get_report(id, list_useful_reviews)
    report['summary'] = get_summary(id, list_useful_reviews)
    report['useful_reports'] = useful_reviews
    report['worker_id'] = id
    workers_info.append(report)
    print(f'done with id: {id}')
e = time.time()


# save worker_info
with open("workers_info.json", "w", encoding="utf-8") as file:
    json.dump(workers_info, file, ensure_ascii=False, indent=4)

print(f"execution time for {len(worker_id_set)} summaries: {e-s}")