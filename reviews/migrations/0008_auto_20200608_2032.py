# Generated by Django 2.2.5 on 2020-06-08 11:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20200608_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
    ]