from django.urls import path

from .views import  getUserStats1, getUserStats2, best_worst_attack, best_worst_defense, viewLevel, homeView, SearchResultsView, getStats, SearchPlayer, createPlayer, deletePlayer, deletePlayer1, deletePlayer2, updatePlayer, addPlayer, addPlayer2, gameSimulator, viewTeammates, getSeasons, deleteAllPlayers1, deleteAllPlayers2, updatePlayer1, updatePlayer2, complexQuery1

urlpatterns = [
    # path('deleteplayer/<str:pk>', deletePlayer, name='delete_form'),

    path('deleteplayer1/<str:pk>', deletePlayer1, name='delete_form1'),
    path('deleteplayer2/<str:pk>', deletePlayer2, name='delete_form2'),

    path('deleteall1', deleteAllPlayers1, name='delete_all1'),
    path('deleteall2', deleteAllPlayers2, name='delete_all2'),

    path('addplayer/<str:pk>/<str:sk>/<str:tk>', addPlayer, name='add_player'),
    path('addplayer2/<str:pk>/<str:sk>/<str:tk>', addPlayer2, name='add_player2'),


    path('simulator', gameSimulator, name='simulate'),

    path('viewteam/<str:pk>/<str:sk>/<str:tk>', viewTeammates, name='teammates'),

    path('seasons/<str:pk>', getSeasons, name='seasons'),

    path('updateplayer1/<str:pk>', updatePlayer1, name='update_form1'),
    path('updateplayer2/<str:pk>', updatePlayer2, name='update_form2'),

    path('complexQuery1', complexQuery1, name='query1'),
    path('viewLevel/<str:pk>/<str:sk>', viewLevel, name='viewLevel'),

    path('complexQuery2a', best_worst_attack, name='attack'),
    path('complexQuery2d', best_worst_defense, name='defense'),


    path('updateplayer/<str:pk>/<str:sk>/<str:tk>', updatePlayer, name='update_form'),

    path('viewstats/<str:pk>/<str:sk>/<str:tk>', getStats, name='stats_page'),
    path('viewuser1stats/<str:pk>/<str:sk>', getUserStats1, name='stats_page_user1'),
    path('viewuser2stats/<str:pk>/<str:sk>', getUserStats2, name='stats_page_user2'),
    # path('viewstats/<str:pk>/<str:sk>/<str:tk>', getStats, name='stats_page'),


    path('insertplayer', createPlayer, name='player_form'),
    path('searchplayer', SearchPlayer.as_view(), name='search_player'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('', homeView, name='home')

]
