from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Task


@register(Task)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'status', 'data']
    # pass
