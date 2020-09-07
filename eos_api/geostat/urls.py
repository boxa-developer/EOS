from django.urls import path
from .views import create_task


urlpatterns = [
    path('task/create', create_task, name='create-task')
]