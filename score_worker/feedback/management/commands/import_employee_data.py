from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from feedback.models import Employee, Feedback, Rating, Summary, SoftSkill, HardSkill

class Command(BaseCommand):
    help = "Fetch worker data from ML API and save to database"

    def handle(self, *args, **kwargs):
        # Define worker ID for example, or loop over all employees as needed
        worker_id = 6135  # Example worker ID
        api_url = f"{settings.API_URL}/worker-data/{worker_id}"

        try:
            # Fetch data from API
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            # Retrieve or create Employee
            employee, _ = Employee.objects.get_or_create(user_id=data["worker_id"])

            # Save Summary
            Summary.objects.update_or_create(
                employee=employee,
                defaults={"summary_text": data["summary"]}
            )

            # Save Rating
            Rating.objects.update_or_create(
                employee=employee,
                defaults={"average_rating": data["score"]}
            )

            # Save SoftSkills
            for skill in data["competencies"]:
                SoftSkill.objects.update_or_create(
                    employee=employee,
                    skill_name=skill["competency"],
                    defaults={"num": skill["score"]}
                )

            # Save HardSkills
            for hard_skill in data["hard_skills"]:
                HardSkill.objects.update_or_create(
                    employee=employee,
                    skill_name=hard_skill
                )

            # Save Feedbacks
            for report in data["useful_reports"]:
                Feedback.objects.update_or_create(
                    employee=employee,
                    employeeTo=report["ID_under_review"],
                    defaults={"feedback_text": report["review"]}
                )

            self.stdout.write(self.style.SUCCESS("Worker data imported successfully"))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"API request failed: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error saving data: {e}"))
