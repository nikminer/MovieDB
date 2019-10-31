# Generated by Django 2.2 on 2019-07-24 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0013_auto_20190724_0500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serial',
            name='episodecount',
        ),
        migrations.RemoveField(
            model_name='serial',
            name='status',
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
                ('episodecount', models.IntegerField()),
                ('serial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.Serial')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Main.StatusList')),
            ],
        ),
    ]