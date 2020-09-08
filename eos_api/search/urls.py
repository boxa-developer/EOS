from django.urls import path
from .views import (
    single_search,
    multi_search,
    search
)


urlpatterns = [
    path('single/<str:dataset_id>', single_search, name='single'),
    path('multi', multi_search, name='multi'),
    path('', search, name='search')
]