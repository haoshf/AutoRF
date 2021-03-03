# Generated by Django 3.0.5 on 2021-01-12 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0006_resource_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='Resource',
        ),
        migrations.AddField(
            model_name='resource',
            name='Resource',
            field=models.CharField(default=None, max_length=128, verbose_name='引用资源'),
            preserve_default=False,
        ),
    ]
