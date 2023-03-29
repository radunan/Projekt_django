# Generated by Django 4.1.4 on 2023-01-18 16:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0008_testuju'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Testuju',
            new_name='PlayerGame',
        ),
        migrations.RenameField(
            model_name='playergame',
            old_name='jedna',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='playergame',
            old_name='dva',
            new_name='player',
        ),
        migrations.AlterField(
            model_name='gameplayer',
            name='game',
            field=models.ManyToManyField(blank=True, null=True, to='games.game'),
        ),
        migrations.AlterField(
            model_name='gameplayer',
            name='player',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]