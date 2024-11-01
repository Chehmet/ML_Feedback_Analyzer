from django.db import models
from django.utils import timezone

class Employee(models.Model):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def update_summary_and_rating(self):
        feedbacks = self.feedback_set.all()
        if feedbacks.exists():
            self.average_rating = sum(f.rating for f in feedbacks) / feedbacks.count()
            self.summary = ' '.join([f.feedback_text for f in feedbacks[:5]])[:500]
            self.save()

class Feedback(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    rating = models.IntegerField()  # Assuming rating is a score from 1 to 5
    date_given = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Feedback for {self.employee.name} - {self.date_given.strftime("%Y-%m-%d")}'
