from django.db import models


class Task(models.Model):
    task_id = models.CharField(max_length=200, blank=False, null=False)
    status = models.CharField(max_length=50, blank=False, null=False)
    req_id = models.CharField(max_length=200, blank=False, null=False)
    task_timeout = models.CharField(max_length=100)
    data = models.JSONField(default=dict)

    def __str__(self):
        return self.task_id

