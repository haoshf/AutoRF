# Generated by Django 3.0.5 on 2021-01-19 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0011_auto_20210118_1145'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='keyword',
            unique_together={('resource', 'keyword_name')},
        ),
        migrations.CreateModel(
            name='Testcase',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('testcase_name', models.CharField(max_length=32, unique=True, verbose_name='用例名称')),
                ('Documentation', models.CharField(max_length=255, verbose_name='关键字描述')),
                ('Setup', models.CharField(max_length=128, verbose_name='参数')),
                ('Teardown', models.CharField(max_length=128, verbose_name='还原操作')),
                ('Return_Value', models.CharField(max_length=128, verbose_name='返回结果')),
                ('Timeout', models.CharField(max_length=32, verbose_name='超时时间')),
                ('Temple', models.CharField(max_length=32, verbose_name='超时时间')),
                ('Tags', models.CharField(max_length=128, verbose_name='标识')),
                ('Table_value', models.TextField(max_length=255, verbose_name='关键字内容')),
                ('create_time', models.DateTimeField(null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(null=True, verbose_name='修改时间')),
                ('sort', models.IntegerField(null=True, verbose_name='排序')),
                ('suite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Suite')),
            ],
            options={
                'db_table': 'testcase',
                'unique_together': {('suite', 'testcase_name')},
            },
        ),
    ]
