from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.detail, name='detail'),
    path('add/', views.add, name='add'),
    path('delete/<int:id>', views.delete, name="delete"),
    path('gameEdit/<int:id>', views.gameEdit, name="gameEdit"),
    path('addGamePlayers/', views.addGamePlayers, name='addGamePlayers'),
]
