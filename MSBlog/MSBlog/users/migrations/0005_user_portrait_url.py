# Generated by Django 2.0.8 on 2018-08-16 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180816_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='portrait_url',
            field=models.URLField(default='https://nmsl.maplewish.cn/msblog/images/portraits/default-portrait.png'),
        ),
    ]
