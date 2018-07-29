# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-29 10:31
from __future__ import unicode_literals

import apps.home.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('banner_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('image', models.ImageField(storage=apps.home.models.ImageStorage(), upload_to='banner/%Y%m%d', verbose_name='轮播图')),
                ('detail_url', models.URLField(verbose_name='访问地址')),
                ('order', models.IntegerField(default=1, verbose_name='顺序')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
                'db_table': 'banner',
            },
        ),
        migrations.CreateModel(
            name='Navigation',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('nav_id', models.AutoField(primary_key=True, serialize=False)),
                ('nav_name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': '导航条',
                'verbose_name_plural': '导航条',
                'db_table': 'navigation',
            },
        ),
    ]
