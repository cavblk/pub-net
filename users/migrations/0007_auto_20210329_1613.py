# Generated by Django 3.1.7 on 2021-03-29 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210324_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuser',
            name='password',
            field=models.CharField(default=None, max_length=128, null=True, verbose_name='password'),
        ),
    ]