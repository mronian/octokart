# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-09 07:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CatalogueItem',
        ),
    ]