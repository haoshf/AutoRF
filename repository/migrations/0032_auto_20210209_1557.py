# Generated by Django 3.0.5 on 2021-02-09 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0031_trigger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trigger',
            name='Cron',
            field=models.CharField(max_length=128, null=True, verbose_name='时间调度'),
        ),
    ]