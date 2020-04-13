# Generated by Django 3.0.4 on 2020-03-28 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlayBooksApp', '0002_auto_20200328_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sectioncontent',
            name='position',
        ),
        migrations.AddField(
            model_name='playbooksection',
            name='section_position',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sectioncontent',
            name='page_position',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
