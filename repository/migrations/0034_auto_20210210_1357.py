# Generated by Django 3.0.5 on 2021-02-10 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0033_auto_20210210_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trigger',
            name='enable',
            field=models.BooleanField(max_length=128, verbose_name='调度状态'),
        ),
    ]
