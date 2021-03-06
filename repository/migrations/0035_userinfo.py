# Generated by Django 3.0.5 on 2021-02-19 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0034_auto_20210210_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('nickname', models.CharField(max_length=32, verbose_name='昵称')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('avatar', models.ImageField(upload_to='', verbose_name='头像')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
    ]
