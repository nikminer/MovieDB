# Generated by Django 2.2.4 on 2019-11-30 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_genrelist_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='img',
            field=models.ImageField(default='default.png', upload_to='Posters'),
        ),
        migrations.AlterField(
            model_name='season',
            name='img',
            field=models.ImageField(default='default.png', upload_to='Posters'),
        ),
        migrations.AlterField(
            model_name='serial',
            name='img',
            field=models.ImageField(default='default.png', upload_to='Posters'),
        ),
    ]