# Generated by Django 3.0.5 on 2021-02-09 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0030_auto_20210207_1112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('trigger_status', models.CharField(max_length=128, verbose_name='调度状态')),
                ('user', models.CharField(max_length=128, verbose_name='配置者')),
                ('Cron', models.CharField(max_length=128, null=True, verbose_name='耗时')),
                ('status', models.CharField(max_length=128, verbose_name='运行状态')),
                ('trigger_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='repository.Project')),
            ],
            options={
                'db_table': 'trigger',
            },
        ),
    ]