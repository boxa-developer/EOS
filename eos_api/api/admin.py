from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Feature


@register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    pass

