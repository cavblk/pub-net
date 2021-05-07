# Generated by Django 3.1.7 on 2021-05-06 14:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20210506_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 6, 15, 26, 43, 257434, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='activation',
            name='token',
            field=models.CharField(default='aa8ae242d416e0769fe64d5342cf8e3550c3262da9ad23dca500aa330fcbcc02', max_length=64),
        ),
    ]
