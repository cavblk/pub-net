# Generated by Django 3.1.7 on 2021-03-29 16:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210329_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(default='ba0a9b4a9d854723dcc4565b28cda7c0e290f25d6ee80daf83c690adfeff68f9', max_length=64)),
                ('expires_at', models.DateTimeField(default=datetime.datetime(2021, 3, 29, 17, 2, 22, 198051, tzinfo=utc))),
                ('activated_at', models.DateTimeField(default=None, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
