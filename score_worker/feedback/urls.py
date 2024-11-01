from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:employee_id>/add_feedback/', views.add_feedback, name='add_feedback'),
]
