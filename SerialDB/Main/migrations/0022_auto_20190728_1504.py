# Generated by Django 2.2.3 on 2019-07-28 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0021_userlist_serial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlist',
            name='userstatus',
            field=models.IntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='UserStatus',
        ),
    ]