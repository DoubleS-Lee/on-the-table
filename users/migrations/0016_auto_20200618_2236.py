# Generated by Django 2.2.5 on 2020-06-18 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20200618_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=80),
        ),
    ]
