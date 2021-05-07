# Generated by Django 3.1.7 on 2021-05-06 10:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210414_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 6, 11, 4, 32, 99041, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='activation',
            name='token',
            field=models.CharField(default='45e2b59a43a9b2fe5b737377d33f6521c6c2e6b87d111ce643a29ffa21bad67b', max_length=64),
        ),
    ]
