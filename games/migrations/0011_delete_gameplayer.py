# Generated by Django 4.1.4 on 2023-04-02 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0010_alter_game_time_end_alter_gameplayer_game_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GamePlayer',
        ),
    ]
