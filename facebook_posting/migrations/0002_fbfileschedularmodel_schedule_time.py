# Generated by Django 3.0.4 on 2020-03-26 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_posting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbfileschedularmodel',
            name='schedule_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
