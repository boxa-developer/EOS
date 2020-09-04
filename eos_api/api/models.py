from django.db import models


class Feature(models.Model):
    f_id = models.CharField(max_length=50, blank=False, null=False)
    feature_version = models.CharField(max_length=50, default='1', blank=False, null=False)
    feature_message = models.CharField(max_length=200, default='message', blank=False, null=False)
    data = models.JSONField(default=dict)   

    def __str__(self):
        return self.f_id


