# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-12 20:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineJudgeApp', '0012_auto_20171107_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='data',
            field=models.FileField(upload_to=b''),
        ),
    ]
