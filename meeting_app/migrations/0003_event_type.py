# Generated by Django 2.2.4 on 2019-10-07 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_app_label', '0002_userprofileinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.CharField(default='case_time_location', max_length=20),
        ),
    ]