# Generated by Django 4.2.3 on 2023-08-01 15:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0004_alter_jobsmodel_logged_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentsmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 31, 55, 273088)),
        ),
        migrations.AlterField(
            model_name='jobsmodel',
            name='logged_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 16, 31, 55, 250886)),
        ),
    ]
