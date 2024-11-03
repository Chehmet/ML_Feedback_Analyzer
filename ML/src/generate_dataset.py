from report_generator import *
from utils import *
import json


dataset = get_all_reviews()

worker_id_set ={56325, 25098, 6159, 6164, 26142, 17439, 31, 37413, 6185, 18480} # store all the worker_ids from dataset
# worker_id_set = set()

# for item in dataset:
#     worker_id_set.add(item['ID_under_review'])

# print(worker_ids)

workers_info = [None for _ in range(len(worker_id_set))]
i = 0

for id in worker_id_set:
    useful_reviews = get_useful_reviews(id)
    list_useful_reviews = [review['review'] for review in useful_reviews]
    report = get_report(id, list_useful_reviews)
    report['summary'] = get_summary(id, list_useful_reviews)
    report['useful_reports'] = useful_reviews
    report['worker_id'] = id
    workers_info[i] = report
    i += 1
    print(f'done with id: {id}')


# save worker_info
with open("workers_info.json", "w", encoding="utf-8") as file:
    json.dump(workers_info, file, ensure_ascii=False, indent=4)
