# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-29 10:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('img_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, max_length=32, verbose_name='图片类型')),
                ('url', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': '商品图片',
                'verbose_name_plural': '商品图片',
                'db_table': 'image',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('property_id', models.AutoField(primary_key=True, serialize=False, verbose_name='商品属性')),
                ('name', models.CharField(max_length=64, verbose_name='属性名称')),
                ('cate', models.ForeignKey(db_column='cate_id', on_delete=django.db.models.deletion.DO_NOTHING, to='category.Category', verbose_name='父菜单')),
            ],
            options={
                'verbose_name': '商品属性',
                'verbose_name_plural': '商品属性',
                'db_table': 'property',
            },
        ),
        migrations.CreateModel(
            name='PropertyValue',
            fields=[
                ('pro_value_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='属性值')),
                ('property', models.ForeignKey(db_column='property_id', on_delete=django.db.models.deletion.CASCADE, to='shop.Property', verbose_name='属性ID')),
            ],
            options={
                'verbose_name': '商品属性值',
                'verbose_name_plural': '商品属性值',
                'db_table': 'property_value',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('shop_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='商品ID')),
                ('name', models.CharField(max_length=100, verbose_name='商品名称')),
                ('sub_title', models.CharField(max_length=255, verbose_name='商品标题')),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='原价')),
                ('promote_price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='折扣价')),
                ('stock', models.IntegerField(verbose_name='库存')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('cate', models.ForeignKey(db_column='cate_id', on_delete=django.db.models.deletion.DO_NOTHING, to='category.Category', verbose_name='商品分类')),
            ],
            options={
                'verbose_name': '商品信息',
                'verbose_name_plural': '商品管理',
                'db_table': 'shop',
            },
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('stock', models.IntegerField(default=0, verbose_name='库存')),
                ('sales', models.IntegerField(default=0, verbose_name='销量')),
                ('sku', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop')),
            ],
            options={
                'db_table': 'sku',
            },
        ),
        migrations.AddField(
            model_name='propertyvalue',
            name='shop',
            field=models.ForeignKey(db_column='shop_id', on_delete=django.db.models.deletion.CASCADE, to='shop.Shop', verbose_name='商品ID'),
        ),
        migrations.AddField(
            model_name='image',
            name='shop',
            field=models.ForeignKey(db_column='shop_id', on_delete=django.db.models.deletion.DO_NOTHING, to='shop.Shop', verbose_name='商品ID'),
        ),
    ]
