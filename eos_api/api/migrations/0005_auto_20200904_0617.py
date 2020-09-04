# Generated by Django 3.1 on 2020-09-04 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200904_0600'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feature',
            old_name='feature_id',
            new_name='f_id',
        ),
        migrations.AddField(
            model_name='feature',
            name='feature_message',
            field=models.CharField(default='message', max_length=200),
        ),
        migrations.AddField(
            model_name='feature',
            name='feature_version',
            field=models.CharField(default='1', max_length=50),
        ),
        migrations.AlterField(
            model_name='feature',
            name='data',
            field=models.JSONField(default=dict),
        ),
    ]