from rest_framework import serializers
from .models import Employee, Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'employee', 'feedback_text', 'rating', 'date_given']

class EmployeeSerializer(serializers.ModelSerializer):
    feedback_set = FeedbackSerializer(many=True, read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'department', 'summary', 'average_rating', 'feedback_set']
