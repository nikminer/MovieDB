# Generated by Django 2.2 on 2019-07-24 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0008_auto_20190724_0355'),
    ]

    operations = [
        migrations.AddField(
            model_name='serial',
            name='disctiption',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='genrelist',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='serial',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='serial',
            name='originalname',
            field=models.TextField(),
        ),
    ]