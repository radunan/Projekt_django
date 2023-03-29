from django import forms
from django.contrib.auth.models import User
from .models import Game


class GameForm(forms.Form):
    title = forms.CharField(max_length=100, label="Název Hry", widget=forms.TextInput(attrs={'class': 'form-control'}))
    time_start = forms.DateTimeField(label="Začátek hry", widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
                                     input_formats=['%d.%m.%Y %H:%M'], required=False)
    time_end = forms.DateTimeField(label="Konec Hry", widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
                                   input_formats=['%d.%m.%Y %H:%M'], required=False)
    description = forms.CharField(label="Popisek Hry", widget=forms.Textarea(attrs={'class': 'form-control'}))
    active = forms.BooleanField(label="Aktivní", required=False,
                                widget=forms.CheckboxInput(attrs={'class': 'form-check-input form-check-label'}))


class GamePlayersForm(forms.Form):
    game = forms.ModelMultipleChoiceField(label="Hra",
                                          queryset=Game.objects.all(),
                                          widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    player = forms.ModelMultipleChoiceField(label="Hráč",
                                            queryset=User.objects.filter(groups__name='Hráč'),
                                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    score = forms.IntegerField(label="Skóre", min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
