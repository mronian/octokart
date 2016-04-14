# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 12:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=50)),
                ('timestamp', models.IntegerField()),
                ('operation', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LockLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=50)),
                ('site_id', models.CharField(max_length=50)),
                ('mode', models.BooleanField(default=False)),
                ('operation', models.CharField(max_length=50)),
                ('timestamp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_id', models.IntegerField()),
                ('mode', models.BooleanField(default=True)),
                ('timestamp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TransactionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=50)),
                ('seller_id', models.IntegerField()),
                ('data_id', models.IntegerField()),
                ('oldvalue', models.IntegerField()),
                ('newvalue', models.IntegerField()),
                ('timestamp', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Log',
        ),
    ]