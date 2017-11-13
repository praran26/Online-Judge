# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-12 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineJudgeApp', '0014_auto_20171113_0205'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='participation',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='participation',
            name='user',
        ),
        migrations.AddField(
            model_name='contest',
            name='ratingUpdated',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Participation',
        ),
    ]
