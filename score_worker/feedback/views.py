from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee, Rating, Summary, SoftSkill, HardSkill, Feedback, Reason
from django.contrib.auth.hashers import check_password
import json

def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        employee = authenticate(request, user_id=user_id, password=password)

        if employee is not None:
            login(request, employee) 
            return redirect('main_page')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)  
    return redirect('login')
 
def main_page(request):
    error_message = None 

    if request.method == 'POST':
        user_id = request.POST.get('user_id')

        try:
            employee = Employee.objects.get(user_id=user_id)
            return redirect('employee_detail', employee_id=employee.id)
        except Employee.DoesNotExist:
            error_message = 'Employee not found'

    return render(request, 'main_page.html', {'error': error_message})


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    summary = Summary.objects.filter(employee=employee).first()
    rating = Rating.objects.filter(employee=employee).first()
    soft_skills = SoftSkill.objects.filter(employee=employee)
    hard_skills = HardSkill.objects.filter(employee=employee)
    soft_skills_data = [skill.num for skill in soft_skills]
    feedback_list = Feedback.objects.filter(employee=employee)
    reason = Reason.objects.filter(employee=employee)
    

    return render(request, 'index.html', {
        'employee': employee,
        'summary': summary,
        'rating': rating.average_rating if rating else None,
        'soft_skills': soft_skills_data,
        'hard_skills': hard_skills, 
        'feedback_list': feedback_list,
        'reason': reason,
    })

def feedback_form(request):
    if request.method == 'POST':
        id_from = request.POST.get('id_from')
        id_to = request.POST.get('id_to')
        feedback_text = request.POST.get('feedback_text')
        
        Feedback.objects.create(employee=Employee.objects.get(user_id=id_from), employeeTo=id_to,
            feedback_text=feedback_text,
        )
        return redirect('main_page')

    return render(request, 'feedback_form.html')
