from django.core.management.base import BaseCommand
from feedback.models import Employee, Feedback

class Command(BaseCommand):
    help = 'Adds test data to the database'

    def handle(self, *args, **kwargs):
        # Clear existing data to avoid duplicates
        Employee.objects.all().delete()
        Feedback.objects.all().delete()

        # Create sample employees
        employee1 = Employee.objects.create(name="Alice Johnson", department="Engineering")
        employee2 = Employee.objects.create(name="Bob Smith", department="Marketing")
        employee3 = Employee.objects.create(name="Charlie Brown", department="Sales")

        # Create feedback for employees
        Feedback.objects.create(employee=employee1, feedback_text="Great work on the project!", rating=5)
        Feedback.objects.create(employee=employee1, feedback_text="Needs improvement in communication.", rating=3)
        Feedback.objects.create(employee=employee2, feedback_text="Outstanding creativity!", rating=4)
        Feedback.objects.create(employee=employee3, feedback_text="Excellent teamwork.", rating=5)

        # Generate summaries and ratings
        for employee in [employee1, employee2, employee3]:
            employee.update_summary_and_rating()

        self.stdout.write(self.style.SUCCESS('Successfully added test data'))
