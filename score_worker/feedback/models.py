from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class Employee(models.Model):
    user_id = models.CharField(max_length=10, default="394")
    password = models.CharField(max_length=128, default=make_password("password123"))
    last_login = models.DateTimeField(null=True, blank=True)

class Feedback(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='feedbacks')
    employeeTo = models.CharField(max_length=10, default="394")
    feedback_text = models.TextField()
    
class Rating(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='rating')
    average_rating = models.FloatField(default=0.0)

class Summary(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='summary')
    summary_text = models.TextField()


class SoftSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='soft_skills')
    skill_name = models.CharField(max_length=50)
    num = models.FloatField(default=0.0)

class HardSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='hard_skills')
    skill_name = models.CharField(max_length=50)

class Reason(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reason')
    reason_text = models.TextField()





