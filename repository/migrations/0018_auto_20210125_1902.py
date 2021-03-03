# Generated by Django 3.0.5 on 2021-01-25 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0017_library'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='documentation',
            field=models.CharField(max_length=255, null=True, verbose_name='方法描述'),
        ),
        migrations.AlterField(
            model_name='library',
            name='filepath',
            field=models.CharField(max_length=32, verbose_name='文件相对路径'),
        ),
        migrations.AlterField(
            model_name='library',
            name='method_name',
            field=models.CharField(max_length=128, verbose_name='函数名称'),
        ),
    ]
