from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from feedback.models import Employee, Feedback, Rating, Summary, SoftSkill, HardSkill, Reason

class Command(BaseCommand):
    help = "Fetch worker data from ML API and save to database"

    def handle(self, *args, **kwargs):
        # Define worker ID for example, or loop over all employees as needed
        # worker_ids = {56325, 25098, 6159, 6164, 26142, 17439, 31, 37413, 6185, 18480, 113201, 32305, 6196, 52276, 24125, 1091, 42056, 11854, 21582, 4179, 20565, 13398, 105560, 25692, 16991, 6247, 11369, 37999, 23153, 10355, 27253, 5750, 23176, 20625, 6293, 23703, 12955, 38045, 162, 18091, 12972, 47280, 26802, 45747, 23220, 30391, 12491, 57549, 19157, 53973, 13525, 12504, 54494, 1764, 57061, 7912, 18154, 55533, 16630, 65282, 54531, 6413, 5390, 5399, 8476, 30493, 36128, 37702, 55112, 55114, 40270, 29007, 24914, 1891, 45416, 15722, 28017, 4978, 53620, 7542, 53626, 20869, 13705, 19851, 57238, 19358, 23971, 20906, 64943, 54705, 23989, 55234, 34246, 57805, 12238, 53199, 6107, 35291, 18404, 90090, 23535, 87536, 15861, 6135, 7162}
        
        worker_ids = {56325, 25098, 6159, 6164, 26142, 17439, 31, 37413, 6185, 18480}
        for id in worker_ids:
            api_url = f"http://127.0.0.1:8001/worker-data/{id}"

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
                    summary_text=data["summary"],
                )

                # Save Rating
                Rating.objects.update_or_create(
                    employee=employee,
                    average_rating=data["score"],
                )

                # Save SoftSkills
                for skill in data["competencies"]:
                    SoftSkill.objects.update_or_create(
                        employee=employee,
                        skill_name=skill["competency"],
                        num=skill["score"],
                    )
                    Reason.objects.update_or_create(
                        employee=employee,
                        reason_text=skill["reason"]
                    )

                # Save HardSkills
                for hard_skill in data["hard_skills"]:
                    HardSkill.objects.update_or_create(
                        employee=employee,
                        skill_name=hard_skill
                    )

                # Save Feedbacks
                for report in data["useful_reviews"]:
                    Feedback.objects.create(
                        employee=employee,
                        employeeTo=report["ID_under_review"],
                        feedback_text=report["review"]
                    )

                # self.stdout.write(self.style.SUCCESS("Worker data imported successfully"))

            except requests.exceptions.RequestException as e:
                self.stderr.write(self.style.ERROR(f"API request failed: {e}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error saving data: {e}"))

        self.stdout.write(self.style.SUCCESS("Worker data imported successfully"))
