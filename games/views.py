from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Game, PlayerGame
from .forms import GameForm, GamePlayersForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


@login_required
def index(request):
    games = Game.objects.all()
    gamePlayers = PlayerGame.objects.all()
    is_admin_or_player = is_player_or_admin(request.user)
    context = {'games': games, 'gameplayers': gamePlayers, 'is_admin_or_player': is_admin_or_player}
    return render(request, 'index.html', context)


@login_required
def detail(request, id):
    game = Game.objects.get(pk=id)
    players = PlayerGame.objects.filter(game=id)
    is_admin_or_player = is_player_or_admin(request.user)
    if request.method == 'POST' and game.active:
        game.time_end = timezone.now()
        game.active = False
        game.save()
    return render(request, 'gameDetail.html',
                  {'game': game, 'players': players, 'is_admin_or_player': is_admin_or_player})


@login_required
def delete(request, id):
    game = Game.objects.get(pk=id)
    game.delete()
    return HttpResponseRedirect('/')


def deletePlayer(request, id):
    gamePlayer = PlayerGame.objects.get(pk=id)
    game_id = gamePlayer.game.id
    gamePlayer.delete()
    return HttpResponseRedirect(reverse('detail', args=[game_id]))


def gameEdit(request, id):
    game = get_object_or_404(Game, id=id)

    if request.method == 'GET':
        form = GameForm(instance=game)
        context = {'form': form, 'id': id, 'game': game}
        return render(request, 'gameEdit.html', context)

    elif request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            context = {'form': form, 'id': id, 'game': game}
            return render(request, 'gameEdit.html', context)


def is_player_or_admin(user):
    if user.is_superuser:
        return user.is_superuser
    else:
        return user.groups.filter(name='Hráč').exists()



@login_required
@user_passes_test(is_player_or_admin, login_url='/')
def add(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            time_start = timezone.now() if form.cleaned_data['active'] else form.cleaned_data['time_start']
            time_end = form.cleaned_data['time_end']
            description = form.cleaned_data['description']
            author = request.user
            active = form.cleaned_data['active']
            Game.objects.create(title=title, time_start=time_start, time_end=time_end, description=description,
                                author=author, active=active)
            return HttpResponseRedirect('/')
    else:
        form = GameForm()

    return render(request, 'gameAdd.html', {'form': form})


@login_required
@user_passes_test(is_player_or_admin, login_url='/')
def addGamePlayers(request):
    if request.method == 'POST':
        form = GamePlayersForm(request.POST)
        if form.is_valid():
            game = form.cleaned_data['game']
            player = form.cleaned_data['player']
            score = form.cleaned_data['score']
            get_player = User.objects.get(username=player[0])
            get_game = Game.objects.get(title=game[0])

            if PlayerGame.objects.filter(game=get_game, player=get_player).exists():
                error_message = f"Hráč {get_player.username} už byl přidán do hry."
                form.add_error('player', error_message)
                return render(request, 'gamePlayersAdd.html', {'form': form})

            PlayerGame.objects.create(game=get_game, player=get_player, score=score)

            return HttpResponseRedirect('/')
    else:
        form = GamePlayersForm()

    return render(request, 'gamePlayersAdd.html', {'form': form})


@login_required
def userGames(request):
    userGames = PlayerGame.objects.filter(player=request.user)
    return render(request, 'user_games.html', {'userGames': userGames})
