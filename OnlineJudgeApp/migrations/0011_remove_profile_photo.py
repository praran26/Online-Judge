# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-06 19:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineJudgeApp', '0010_regnconfirm_hashval'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='photo',
        ),
    ]