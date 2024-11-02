from summary_generator import generate_summary
from competency_scoring import evaluate_competencies
from hard_skills_generator import extract_hard_skills
from utils import *
from dotenv import load_dotenv

load_dotenv()
api = os.getenv("API_URL")


def get_summary(worker_id, reviews=None):
    if not reviews:
        reviews = get_reviews(worker_id)
    return generate_summary(reviews, api)


def get_competencies(worker_id, reviews=None):
    if not reviews:
        reviews = get_reviews(worker_id)
    return evaluate_competencies(reviews, api)


def get_hardskills(worker_id, reviews=None):
    if not reviews:
        reviews = get_reviews(worker_id)
    return extract_hard_skills(reviews, api)


def calculate_score(competencies):
    total_score = 0
    for competency in competencies:
        total_score += competency['score']
    return total_score / len(competencies)


def get_report(worker_id):
    reviews = get_reviews(worker_id)

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
print(get_summary(id))
# print(get_competencies(id))
# print(get_hardskills(id))

print(get_report(id))
