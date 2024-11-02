from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import Employee

class EmployeeBackend(ModelBackend):
    def authenticate(self, request, user_id=None, password=None, **kwargs):
        try:
            employee = Employee.objects.get(user_id=user_id)
            if check_password(password, employee.password):
                return employee
        except Employee.DoesNotExist:
            return None
