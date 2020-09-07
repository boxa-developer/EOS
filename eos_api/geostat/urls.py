from django.urls import path
from .views import create_task, check_status


urlpatterns = [
    path('task/create', create_task, name='create-task'),
    path('task/<str:task_id>', check_status, name='check-status')
]