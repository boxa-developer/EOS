# Generated by Django 3.1 on 2020-09-08 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_feature_api_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=50)),
                ('req_id', models.CharField(max_length=200)),
                ('task_timeout', models.CharField(max_length=100)),
                ('data', models.JSONField(default=dict)),
            ],
        ),
    ]