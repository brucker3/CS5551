# Generated by Django 3.1.1 on 2020-11-06 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkers', '0015_delete_game_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game_Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.CharField(max_length=255)),
                ('player1_usrname', models.CharField(max_length=255)),
                ('player2_username', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
