# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-18 04:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0003_auto_20170504_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicgroup',
            name='dekid',
            field=models.IntegerField(default=0, verbose_name='ID в Деканате'),
        ),
    ]
