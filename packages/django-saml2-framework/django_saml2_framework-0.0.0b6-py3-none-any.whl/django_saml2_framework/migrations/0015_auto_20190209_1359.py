# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-09 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_saml2_framework', '0014_auto_20190207_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='identityprovider',
            name='use_custom_maps',
            field=models.BooleanField(default=True, help_text='use custom mapping models'),
        ),
        migrations.AddField(
            model_name='identityprovider',
            name='use_django_maps',
            field=models.BooleanField(default=True, help_text='Use the custom mapping for django'),
        ),
        migrations.AddField(
            model_name='identityprovider',
            name='use_pysaml_maps',
            field=models.BooleanField(default=True, help_text='todo: put link to docs'),
        ),
        migrations.AddField(
            model_name='serviceprovider',
            name='use_custom_maps',
            field=models.BooleanField(default=True, help_text='use custom mapping models'),
        ),
        migrations.AddField(
            model_name='serviceprovider',
            name='use_django_maps',
            field=models.BooleanField(default=True, help_text='Use the custom mapping for django'),
        ),
        migrations.AddField(
            model_name='serviceprovider',
            name='use_pysaml_maps',
            field=models.BooleanField(default=True, help_text='todo: put link to docs'),
        ),
    ]
