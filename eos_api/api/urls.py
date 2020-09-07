from django.urls import path
from .views import (
    collection,
    history_by_id,
    feature_by_id,
    feature_by_key,
    feature_by_point,
    create_feature,
    modify_feature,
    delete_feature,
    all_features
)


urlpatterns = [
    path('collection', collection, name='collection'),
    path('feature/<int:id>', feature_by_id, name='feature'),
    path('history/<int:id>', history_by_id, name='history'),
    path('feature?key=<str:key>', feature_by_key, name='feature-key'),
    path('feature?point=<str:point>', feature_by_point, name='feature-point'),
    path('create', create_feature, name='create'),
    path('modify', modify_feature, name='modify'),
    path('delete', delete_feature, name='delete'),
    path('all', all_features, name='all')
]