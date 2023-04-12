from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Game, PlayerGame
from .forms import GameForm, GamePlayersForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

"""
from django.contrib.auth import get_user_model
User = get_user_model()"""


@login_required
def index(request):
    games = Game.objects.all().order_by('-time_start')
    gamePlayers = PlayerGame.objects.all()                          #výpis hráčů na indexu
    is_admin_or_player = is_player_or_admin(request.user)
    context = {'games': games, 'gameplayers': gamePlayers, 'is_admin_or_player': is_admin_or_player}
    return render(request, 'index.html', context)


@login_required
def detail(request, id):
    game = Game.objects.get(pk=id)
    players = PlayerGame.objects.filter(game=id)                #detail hry
    is_admin_or_player = is_player_or_admin(request.user)

    if request.method == 'POST' and game.active:
        game.time_end = timezone.now()
        game.active = False

        winner = game.get_winner()
        winner_name = winner.username if winner else None         #získávání výherce hry
        game.winner = winner_name
        game.save()

    return render(request, 'gameDetail.html',
                  {'game': game, 'players': players, 'is_admin_or_player': is_admin_or_player,
                   'winner': str(game.winner)})


@login_required
def delete(request, id):
    game = Game.objects.get(pk=id)
    game.delete()                           #mazání her
    return HttpResponseRedirect('/')


def deletePlayer(request, id):
    gamePlayer = PlayerGame.objects.get(pk=id)
    game_id = gamePlayer.game.id                    #mazání hráčů ve hře
    is_current_winner = False

    game = Game.objects.get(id=game_id)
    if game.winner == gamePlayer.player.username:
        is_current_winner = True

    gamePlayer.delete()

    if is_current_winner:
        winner = game.get_winner()
        if winner:
            game.winner = winner.playergame_set.first().player.username         #pokud je mazaný hráč výherce musí se přepnout vítěz
        else:
            game.winner = None
        game.save()

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
    if user.is_superuser:                   #funkce na určení zda je užívatel admin nebo hráč
        return user.is_superuser
    else:
        return user.groups.filter(name='Hráč').exists()


@login_required
@user_passes_test(is_player_or_admin, login_url='/')
def add(request):                                                   #přidávání her
    active_games = Game.objects.filter(active=True).count()

    if active_games >= 2 and request.POST.get('active'):
        error_message = "Nelze mít více než 2 aktivní hry. Vydrž než hry skončí :)"       #počet aktivních her nesmí být větší než 2
        return render(request, 'gameAdd.html', {'form': GameForm(), 'error_message': error_message})

    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            time_start = timezone.now() if form.cleaned_data['active'] else form.cleaned_data['time_start']    #pokud je hra aktivní nastaví se aktuální čas
            time_end = form.cleaned_data['time_end']
            description = form.cleaned_data['description']
            author = request.user
            active = form.cleaned_data['active']
            game = Game.objects.create(title=title, time_start=time_start, time_end=time_end, description=description,
                                       author=author, active=active)
            return HttpResponseRedirect(reverse('detail', args=[game.id]))
    else:
        form = GameForm()

    return render(request, 'gameAdd.html', {'form': form})


@login_required
@user_passes_test(is_player_or_admin, login_url='/')
def addGamePlayers(request):                #přidávání hráčů do hry
    if request.method == 'POST':
        form = GamePlayersForm(request.POST)
        if form.is_valid():
            game = form.cleaned_data['game']
            player = form.cleaned_data['player']
            score = form.cleaned_data['score']
            get_player = User.objects.get(username=player[0])
            get_game = Game.objects.get(title=game[0])

            if PlayerGame.objects.filter(game=get_game, player=get_player).exists():      #pokud hráč se ve hře nachází, už nelze přidat
                error_message = f"Hráč {get_player.username} už byl přidán do hry."
                form.add_error('player', error_message)
                return render(request, 'gamePlayersAdd.html', {'form': form})

            PlayerGame.objects.create(game=get_game, player=get_player, score=score)

            if not get_game.active:
                winner = get_game.get_winner()
                get_game.winner = winner.playergame_set.first().player.username         #nastavování výherce pokud hra neni aktivní
                get_game.save()

            return HttpResponseRedirect(reverse('detail', args=[get_game.pk]))
    else:
        form = GamePlayersForm()

    return render(request, 'gamePlayersAdd.html', {'form': form})


@login_required
@user_passes_test(is_player_or_admin, login_url='/')
def userGames(request):
    userGames = PlayerGame.objects.filter(player=request.user).order_by('-game__time_start')                  #historie hráče
    return render(request, 'user_games.html', {'userGames': userGames})
