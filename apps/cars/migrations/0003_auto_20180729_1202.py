# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-29 12:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
        ('cars', '0002_shopcar_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcar',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.Shop', verbose_name='商品ID'),
        ),
        migrations.AddField(
            model_name='shopcar',
            name='user',
            field=models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='用户ID'),
        ),
    ]