# Generated by Django 2.2 on 2019-07-24 01:54

import Main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_auto_20190724_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serial',
            name='status',
            field=models.IntegerField(default=1, verbose_name=Main.models.StatusList),
        ),
    ]