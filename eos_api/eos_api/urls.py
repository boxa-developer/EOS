from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('feature/', include('api.urls')),
    path('search/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('stat/', include('api.urls')),
]
