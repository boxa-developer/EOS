from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Feature, Task


@register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['f_id', 'api_key', 'feature_version', 'feature_message', 'data']


@register(Task)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'status', 'data']
