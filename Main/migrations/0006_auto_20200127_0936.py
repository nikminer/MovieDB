# Generated by Django 3.0.2 on 2020-01-27 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_auto_20200126_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genref',
            name='film',
        ),
        migrations.RemoveField(
            model_name='genref',
            name='genre',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='GenreF',
        ),
        migrations.DeleteModel(
            name='GenreList',
        ),
    ]