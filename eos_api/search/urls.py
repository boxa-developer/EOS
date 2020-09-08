from django.urls import path
from .views import (
    single_search
)


urlpatterns = [
    path('single/<str:dataset_id>', single_search, name='single'),

]