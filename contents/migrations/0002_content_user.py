# Generated by Django 2.2.5 on 2020-06-15 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contents', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='user',
            field=models.ForeignKey(help_text='작성자', on_delete=django.db.models.deletion.CASCADE, related_name='contents', to=settings.AUTH_USER_MODEL),
        ),
    ]
