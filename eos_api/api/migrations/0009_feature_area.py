# Generated by Django 3.1 on 2020-09-25 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='area',
            field=models.CharField(default='Not Calculated', max_length=200),
        ),
    ]