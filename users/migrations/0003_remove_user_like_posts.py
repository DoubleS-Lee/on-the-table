# Generated by Django 2.2.5 on 2020-05-09 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_like_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='like_posts',
        ),
    ]