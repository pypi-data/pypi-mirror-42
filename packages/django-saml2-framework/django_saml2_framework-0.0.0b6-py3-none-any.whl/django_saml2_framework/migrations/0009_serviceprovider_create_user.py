# Generated by Django 2.1.5 on 2019-02-04 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_saml2_framework', '0008_auto_20190204_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprovider',
            name='create_user',
            field=models.BooleanField(blank=True, default=False, help_text='If checked the SP will try to create new user accounts.'),
        ),
    ]
