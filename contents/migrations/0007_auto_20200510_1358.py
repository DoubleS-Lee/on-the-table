# Generated by Django 2.2.5 on 2020-05-10 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0006_auto_20200510_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='cooking_utensils',
            field=models.ManyToManyField(blank=True, related_name='contents', to='contents.CookingUtensil'),
        ),
        migrations.AlterField(
            model_name='content',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='photo',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='contents.Content'),
        ),
    ]
