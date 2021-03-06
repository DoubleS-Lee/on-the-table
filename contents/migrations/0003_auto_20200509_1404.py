# Generated by Django 2.2.5 on 2020-05-09 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0002_auto_20200509_1326'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CookingUtesil',
            new_name='CookingUtensil',
        ),
        migrations.AlterModelOptions(
            name='cookingutensil',
            options={'ordering': ['name'], 'verbose_name_plural': 'CookingUtensils'},
        ),
        migrations.RemoveField(
            model_name='content',
            name='dish_photos',
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('caption', models.CharField(max_length=80)),
                ('file', models.ImageField(upload_to='')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contents.Content')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
