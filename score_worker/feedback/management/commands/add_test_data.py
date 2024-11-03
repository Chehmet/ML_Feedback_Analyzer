# feedback/management/commands/add_test_data.py

from django.core.management.base import BaseCommand
from feedback.models import Employee, Summary, SoftSkill, HardSkill, Feedback
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Adds test data to the database'

    def handle(self, *args, **kwargs):
        # Clear existing data to avoid duplicates
        Employee.objects.all().delete()
        Feedback.objects.all().delete()
        Summary.objects.all().delete()
        SoftSkill.objects.all().delete()
        HardSkill.objects.all().delete()

        # Create sample employees with user_id and password
        employee1 = Employee.objects.create(user_id="394", password=make_password("password394"))
        employee2 = Employee.objects.create(user_id="274", password=make_password("password274")) 
        employee3 = Employee.objects.create(user_id="8800", password=make_password("password8800"))

        # Create feedback for employees
        Feedback.objects.create(employee=employee1, employeeTo="274", feedback_text="Great work on the project!")
        Feedback.objects.create(employee=employee1, employeeTo="8800", feedback_text="Needs improvement in communication.")
        Feedback.objects.create(employee=employee2, employeeTo="394", feedback_text="Outstanding creativity!")
        Feedback.objects.create(employee=employee3, employeeTo="274", feedback_text="Excellent teamwork.")

        # Create summaries for employees
        Summary.objects.create(employee=employee1, summary_text="Alice has shown excellent problem-solving skills.")
        Summary.objects.create(employee=employee2, summary_text="Bob is very creative and brings new ideas to the team.")
        Summary.objects.create(employee=employee3, summary_text="Charlie is a team player and contributes greatly to group projects.")

        # Create soft skills for employees with `num` values
        SoftSkill.objects.create(employee=employee1, skill_name="Коммуникация", num=4.5)
        SoftSkill.objects.create(employee=employee1, skill_name="Работа в команде", num=3.8)
        SoftSkill.objects.create(employee=employee1, skill_name="Профессионализм", num=4.0)
        SoftSkill.objects.create(employee=employee2, skill_name="Инициативность", num=4.7)
        SoftSkill.objects.create(employee=employee2, skill_name="Саморазвитие", num=4.7)
        SoftSkill.objects.create(employee=employee2, skill_name="Решительность", num=4.4)
        SoftSkill.objects.create(employee=employee3, skill_name="Адаптивность", num=4.0)
        SoftSkill.objects.create(employee=employee3, skill_name="Лидерство", num=3.5)
        SoftSkill.objects.create(employee=employee3, skill_name="Ответственность", num=3.5)
        SoftSkill.objects.create(employee=employee3, skill_name="Коммуникация", num=3.5)


        # Create hard skills for employees
        HardSkill.objects.create(employee=employee1, skill_name="Python")
        HardSkill.objects.create(employee=employee1, skill_name="Django")
        HardSkill.objects.create(employee=employee2, skill_name="SEO")
        HardSkill.objects.create(employee=employee3, skill_name="Sales Strategy")

        self.stdout.write(self.style.SUCCESS('Successfully added test data'))
