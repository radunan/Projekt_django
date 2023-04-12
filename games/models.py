from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

"""from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    credits = models.IntegerField(default=100)"""


class Game(models.Model):
    title = models.CharField('Titulek', max_length=100)
    time_start = models.DateTimeField('Čas zahájení')
    time_end = models.DateTimeField('Čas ukončení', blank=True, null=True)
    description = models.TextField('Popisek', max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField('Aktivní', default=False)
    winner = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_winner(self):
        winner = self.playergame_set.aggregate(Max('score'))
        max_score = winner['score__max']
        if max_score is None:
            return None
        winner_player = self.playergame_set.filter(score=max_score).first().player
        return winner_player


class PlayerGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField('skóre', default=0)

    def __str__(self):
        return f'{self.game.title}: {self.player.username}'
