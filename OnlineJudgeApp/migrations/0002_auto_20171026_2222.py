# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-26 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineJudgeApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='users'),
        ),
    ]