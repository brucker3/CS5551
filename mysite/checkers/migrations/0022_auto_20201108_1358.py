# Generated by Django 3.1.1 on 2020-11-08 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkers', '0021_auto_20201108_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game_session',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
