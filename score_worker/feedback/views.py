from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee, Feedback

def index(request):
    query = request.GET.get('search', '')
    employees = Employee.objects.filter(name__icontains=query) if query else Employee.objects.all()
    return render(request, 'index.html', {'employees': employees, 'query': query})

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'employee_detail.html', {'employee': employee})

def add_feedback(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        feedback_text = request.POST['feedback_text']
        rating = int(request.POST['rating'])
        Feedback.objects.create(employee=employee, feedback_text=feedback_text, rating=rating)
        employee.update_summary_and_rating()
        return redirect('employee_detail', employee_id=employee.id)
    return render(request, 'feedback_form.html', {'employee': employee})
