from django.urls import path
from .views import (
    collect_view,
    history_view,
    feature_view
)


urlpatterns = [
    path('collection/', collect_view, name='collection'),
    path('feature/', feature_view, name='feature'),
    path('history/', history_view, name='history'),
]