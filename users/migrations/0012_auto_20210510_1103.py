# Generated by Django 3.1.7 on 2021-05-10 09:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210506_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 9, 33, 13, 5874, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='activation',
            name='token',
            field=models.CharField(default='6b49313d8fbea08c15be798071e3bdfb532f3a229a5edfda6234e323c347d92d', max_length=64),
        ),
    ]
