# Generated by Django 2.2.5 on 2020-06-08 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20200605_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(blank=True, null=True),
        ),
    ]