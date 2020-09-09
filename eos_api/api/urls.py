from django.urls import path
from .views.geometry_views import (
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
from .views.stat_views import (
    create_task,
    check_status
)
from .views.search_views import (
    single_search,
    multi_search,
    search
)

from .views.weather_views import (
    weather_forecast_data,
    weather_forecast,
    weather_history
)

from .views.tile_views import (
    multi_spectral_tile
)

urlpatterns = [
                  # Geometry Storage API URLs
                  path('feature/collection', collection, name='collection'),
                  path('feature/<int:id>', feature_by_id, name='feature'),
                  path('feature/<int:id>/history', history_by_id, name='history'),
                  path('feature?key=<str:key>', feature_by_key, name='feature-key'),
                  path('feature?point=<str:point>', feature_by_point, name='feature-point'),
                  path('feature/create', create_feature, name='create'),
                  path('feature/modify', modify_feature, name='modify'),
                  path('feature/delete', delete_feature, name='delete'),
                  path('feature/all', all_features, name='all')
              ] + \
              [
                  # Statistic API URLs
                  path('task/create', create_task, name='create-task'),
                  path('task/status/<str:task_id>', check_status, name='check-status')
              ] + \
              [
                  # Search API URLs
                  path('search/single/<str:dataset_id>', single_search, name='single'),
                  path('search/multi', multi_search, name='multi'),
                  path('search', search, name='search')
              ] + \
              [
                  # Weather API URLs
                  path('weather/data', weather_forecast_data, name='with_data'),
                  path('weather', weather_forecast, name='no_data'),
                  path('weather/history', weather_history, name='history')
              ] + \
              [
                  # Tile API URLs
                  path('tile/multisp', multi_spectral_tile, name='multisp')
              ]
