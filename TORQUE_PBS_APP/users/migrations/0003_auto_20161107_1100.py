# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-07 11:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_has_system_acount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='customuser',
            unique_together=set([('email',)]),
        ),
    ]
