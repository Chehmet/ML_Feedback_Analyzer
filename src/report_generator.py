from summary_generator import generate_summary
from competency_scoring import evaluate_competencies
from hard_skills_generator import extract_hard_skills
from utils import *
from dotenv import load_dotenv
import time


load_dotenv()
api = os.getenv("API_URL")


def get_summary(worker_id, reviews=None):
    if not reviews:
        reviews = get_list_useful_reviews(worker_id)
    return generate_summary(reviews, api)


def get_competencies(worker_id, reviews=None):
    if not reviews:
        reviews = get_list_useful_reviews(worker_id)
    return evaluate_competencies(reviews, api)


def get_hardskills(worker_id, reviews=None):
    if not reviews:
        reviews = get_list_useful_reviews(worker_id)
    return extract_hard_skills(reviews, api)


def calculate_score(competencies):
    total_score = 0
    for competency in competencies:
        if competency['score']:
            total_score += competency['score']
    return total_score / len(competencies)


def get_report(worker_id, reviews=None):
    if not reviews:
        reviews = get_list_useful_reviews(worker_id)

    competencies = get_competencies(id, reviews)
    hard_skills = get_hardskills(id, reviews)
    score = calculate_score(competencies)

    data = {
        'competencies': competencies,
        'hard skills' : hard_skills,
        'score' : score,
    }

    return data


id = 6135

s = time.time()
reviews = get_list_useful_reviews(id)
u = time.time()
print(get_summary(id, reviews))
m = time.time()
print(get_report(id, reviews))
e = time.time()

print(f"Useful reviews retrieval time: {u-s:.2f}")
print(f"Summary generation time: {m-u:.2f}")
print(f"Rest of report generation time: {e-m:.2f}")
print(f"Whole report generation time: {e-s:.2f}")
