# Generated by Django 2.2.5 on 2020-05-12 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0008_auto_20200510_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='country_of_dish',
        ),
    ]