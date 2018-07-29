# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-29 10:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('cate_id', models.AutoField(primary_key=True, serialize=False, verbose_name='分类ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='名称')),
            ],
            options={
                'verbose_name': '分类菜单',
                'verbose_name_plural': '分类菜单',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='SubMenu',
            fields=[
                ('sub_menu_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('cate', models.ForeignKey(db_column='cate_id', on_delete=django.db.models.deletion.DO_NOTHING, to='category.Category', verbose_name='父菜单')),
            ],
            options={
                'verbose_name': '一级菜单',
                'verbose_name_plural': '一级菜单',
                'db_table': 'sub_menu',
            },
        ),
        migrations.CreateModel(
            name='TwoMenu',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('sub_menu2_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('sub_menu', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='category.SubMenu', verbose_name='一级菜单')),
            ],
            options={
                'verbose_name': '二级菜单',
                'verbose_name_plural': '二级菜单',
                'db_table': 'two_menu',
            },
        ),
    ]