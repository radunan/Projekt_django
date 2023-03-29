# Generated by Django 4.1.4 on 2023-01-18 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0003_gameplayer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.TextField(max_length=250, verbose_name='Popisek'),
        ),
        migrations.RemoveField(
            model_name='gameplayer',
            name='game',
        ),
        migrations.RemoveField(
            model_name='gameplayer',
            name='player',
        ),
        migrations.AddField(
            model_name='gameplayer',
            name='game',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='games.game'),
        ),
        migrations.AddField(
            model_name='gameplayer',
            name='player',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]