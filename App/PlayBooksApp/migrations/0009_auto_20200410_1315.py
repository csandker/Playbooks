# Generated by Django 3.0.4 on 2020-04-10 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlayBooksApp', '0008_remove_playpage_included_folder_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playpage',
            name='check_updates',
            field=models.BooleanField(default=False),
        ),
    ]
