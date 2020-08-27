from django.urls import path
from .views import (
    collect_view,
    history_view,
    feature_view,
    create_feature,
    modify_feature,
    delete_feature
)


urlpatterns = [
    path('collection/', collect_view, name='collection'),
    path('feature/', feature_view, name='feature'),
    path('history/', history_view, name='history'),
    path('create/', create_feature, name='create'),
    path('modify/', modify_feature, name='modify'),
    path('delete/', delete_feature, name='delete')
]