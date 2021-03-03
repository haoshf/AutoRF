# Generated by Django 3.0.5 on 2021-02-22 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0036_auto_20210219_1522'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='userinfo',
            table='userInfo',
        ),
        migrations.CreateModel(
            name='Smtp',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('mail_host', models.CharField(max_length=64, verbose_name='密码')),
                ('mail_user', models.EmailField(max_length=32, verbose_name='发件人邮箱')),
                ('mail_pass', models.CharField(max_length=64, verbose_name='邮箱授权码')),
                ('receivers', models.TextField(verbose_name='收件人')),
                ('cc', models.TextField(null=True, verbose_name='抄送人')),
                ('enable', models.BooleanField(max_length=32, verbose_name='开关状态')),
                ('title', models.TextField(verbose_name='邮件主题')),
                ('documentation', models.TextField(verbose_name='邮件内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(null=True, verbose_name='修改时间')),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='repository.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='repository.UserInfo')),
            ],
            options={
                'db_table': 'smtp',
            },
        ),
    ]
