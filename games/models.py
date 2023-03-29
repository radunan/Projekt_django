from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    title = models.CharField('Titulek', max_length=100)
    time_start = models.DateTimeField('Čas zahájení')
    time_end = models.DateTimeField('Čas ukončení', blank=True, null=True)
    description = models.TextField('Popisek', max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField('Aktivní', default=False)

    def __str__(self):
        return self.title


class GamePlayer(models.Model):
    game = models.ManyToManyField(Game, blank=True)
    player = models.ManyToManyField(User, blank=True)
    score = models.IntegerField('skóre', default=0)

    def __str__(self):
        return "Hráči ve Hrách + body"


class PlayerGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField('skóre', default=0)

    def __str__(self):
        return "Hráči ve Hrách + body"
