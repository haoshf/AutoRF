# Generated by Django 3.0.5 on 2021-01-11 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='suite',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='repository.Project'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='project',
            name='Resource',
        ),
        migrations.AddField(
            model_name='project',
            name='Resource',
            field=models.CharField(default=None, max_length=128, verbose_name='引用资源'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='suite',
            name='Resource',
        ),
        migrations.AddField(
            model_name='suite',
            name='Resource',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='repository.Resource'),
        ),
    ]