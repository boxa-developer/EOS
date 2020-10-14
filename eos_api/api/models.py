from django.db import models


#   Feature Model
class Feature(models.Model):
    f_id = models.CharField(max_length=50, blank=False, null=False, unique=True)
    api_key = models.CharField(max_length=300, blank=False, null=False,
                               default='ApiKey apk.ab435aa666ab42ccc6e4220270e35d9a79ed678fe983b739bd465b5965f61e9c')
    feature_version = models.CharField(max_length=50, default='1', blank=False, null=False)
    feature_message = models.CharField(max_length=200, default='message', blank=False, null=False)
    data = models.JSONField(default=dict)
    area = models.CharField(max_length=200, default='Not Calculated')

    def __str__(self):
        return self.f_id


# Export Features Model
class EFeature(models.Model):
    export_id = models.CharField(max_length=20, blank=False, null=False)
    farmer_id = models.CharField(max_length=20, blank=False, null=False)
    polygon = models.JSONField(dict())
    feature_data = models.JSONField(dict())
    created_date = models.DateTimeField(auto_now=True)
    properties = models.JSONField(dict())
    crop_type = models.IntegerField()
    contour_number = models.IntegerField()

    def __str__(self):
        return f'Fermer #{self.farmer_id} ID: {self.export_id}'


# Task Model
class Task(models.Model):
    task_id = models.CharField(max_length=200, blank=False, null=False)
    status = models.CharField(max_length=50, blank=False, null=False)
    req_id = models.CharField(max_length=200, blank=False, null=False)
    task_timeout = models.CharField(max_length=100)
    data = models.JSONField(default=dict)

    def __str__(self):
        return self.task_id


