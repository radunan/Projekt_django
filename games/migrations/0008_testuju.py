# Generated by Django 4.1.4 on 2023-01-18 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0007_remove_gameplayer_game_remove_gameplayer_player_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testuju',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, verbose_name='skóre')),
                ('dva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('jedna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
            ],
        ),
    ]