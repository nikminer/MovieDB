# Generated by Django 2.2 on 2019-07-24 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0015_auto_20190724_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
    ]