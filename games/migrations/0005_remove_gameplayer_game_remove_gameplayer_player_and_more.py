# Generated by Django 4.1.4 on 2023-01-18 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0004_alter_game_description_remove_gameplayer_game_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameplayer',
            name='game',
        ),
        migrations.RemoveField(
            model_name='gameplayer',
            name='player',
        ),
        migrations.CreateModel(
            name='PlayerGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, verbose_name='skóre')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gameplayer',
            name='game',
            field=models.ManyToManyField(to='games.game'),
        ),
        migrations.AddField(
            model_name='gameplayer',
            name='player',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]