from django.db import models


class Feature(models.Model):
    feature_id = models.CharField(max_length=50)
    feature_version = models.CharField(max_length=50)
    feature_message = models.CharField(max_length=200)
    data = models.JSONField(default=dict)

    def __str__(self):
        return self.feature_id


