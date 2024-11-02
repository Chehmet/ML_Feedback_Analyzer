from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee, Rating, Summary, SoftSkill, HardSkill
from django.contrib.auth.hashers import check_password
import json

def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        # Authenticate the user
        employee = authenticate(request, user_id=user_id, password=password)

        if employee is not None:
            login(request, employee)  # This sets the session
            return redirect('main_page')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)  # Clears the session data
    return redirect('login')

# Main page with search (only accessible if logged in)
 
def main_page(request):
    error_message = None  # Initialize error message variable

    if request.method == 'POST':
        user_id = request.POST.get('user_id')

        # Check if employee exists
        try:
            employee = Employee.objects.get(user_id=user_id)
            return redirect('employee_detail', employee_id=employee.id)
        except Employee.DoesNotExist:
            error_message = 'Employee not found'  # Set error message

    return render(request, 'main_page.html', {'error': error_message})


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    summary = Summary.objects.filter(employee=employee).first()
    rating = Rating.objects.filter(employee=employee).first()
    soft_skills = SoftSkill.objects.filter(employee=employee)
    hard_skills = HardSkill.objects.filter(employee=employee)

    soft_skills_data = [skill.num for skill in soft_skills]
    

    return render(request, 'employee_detail.html', {
        'employee': employee,
        'summary': summary,
        'rating': rating.average_rating if rating else None,
        'soft_skills': soft_skills_data,
        'hard_skills': hard_skills
    })
