# cities/views.py
from django.views.generic import TemplateView, ListView, FormView

from django.shortcuts import redirect

from django.shortcuts import render

from .forms import PlayersForm, UpdateForm, DeleteForm, StatsForm, UserForm1, UserForm2

from .models import Players, SearchPlayers, Teams, Stats, UserPlayers, User2, User1Stats, User2Stats

from django.db.models import Q # new

from tablib import Dataset

import mysql.connector

import logging

import numpy as np

import random as rnd

from neo4j import GraphDatabase

import copy

import math

def complexQuery1(request):
    players = Players.objects.raw('''
    SELECT * FROM NBA.Player
WHERE points > 1500 AND points < 2000 AND (team_id, season_id) IN (SELECT team_id, season_id FROM NBA.Player WHERE season_id IN ("1988-89","1989-90"))
''')
    context = {'object_list':players}
    return render(request, 'search_results.html', context)

def viewLevel(request, pk, sk):
    lower = int(pk) - 250
    higher = int(pk) + 250
    print(lower, higher)
    players = Players.objects.raw('''
    SELECT * FROM NBA.Player JOIN NBA.Teams ON NBA.Player.team_id = NBA.Teams.id
WHERE points > %s AND points < %s AND (team_id, season_id) IN (SELECT team_id, season_id FROM NBA.Player WHERE season_id = %s)
ORDER BY points ASC
''', [lower, higher, sk])
    context = {'object_list':players}
    return render(request, 'search_results.html', context)

def best_worst_attack(request):
    teams = Teams.objects.raw('''
        (SELECT team_name, season_id, id FROM NBA.Stats JOIN NBA.Teams ON NBA.Teams.id = NBA.Stats.team_id GROUP BY team_id, season_id ORDER BY SUM(FG3_PCT) DESC, SUM(FG_PCT) DESC, SUM(AST) DESC, SUM(OREB) DESC LIMIT 5)
        UNION
        (SELECT team_name, season_id, id FROM NBA.Stats JOIN NBA.Teams ON NBA.Teams.id = NBA.Stats.team_id GROUP BY team_id, season_id ORDER BY SUM(FG3_PCT) ASC, SUM(FG_PCT) ASC, SUM(AST) ASC, SUM(OREB) ASC LIMIT 5)
                                ''')
    offense = 'Offense'
    context = {'object_list':teams, 'offense':offense}
    return render(request, 'complex2.html', context)

def best_worst_defense(request):
    teams = Teams.objects.raw('''
        (SELECT team_name, season_id, id FROM NBA.Stats JOIN NBA.Teams ON NBA.Teams.id = NBA.Stats.team_id GROUP BY team_id, season_id ORDER BY SUM(DREB) DESC, SUM(STL) DESC, SUM(BLK) DESC LIMIT 5)
        UNION
        (SELECT team_name, season_id, id FROM NBA.Stats JOIN NBA.Teams ON NBA.Teams.id = NBA.Stats.team_id GROUP BY team_id, season_id ORDER BY SUM(DREB) ASC, SUM(STL) ASC, SUM(BLK) ASC LIMIT 5)
                                ''')
    defense = 'Defense'
    context = {'object_list':teams, 'defense':defense}
    return render(request, 'complex2.html', context)

def homeView(request):
    players = User1Stats.objects.raw('SELECT * FROM user1stats JOIN Teams ON user1stats.team_id = Teams.id')
    team2 = User2Stats.objects.raw('SELECT * FROM user2stats JOIN Teams ON user2stats.team_id = Teams.id')
    context = {'players':players, 'opponents':team2}
    return render(request, 'home.html', context)

class HomePageView(TemplateView):
    template_name = 'home.html'
    players = UserPlayers.objects.all()
    context = {'players':players}

class SearchPlayer(TemplateView):
    template_name = 'search.html'

class PlayersFormView(FormView):
    form_class = PlayersForm
    template_name = 'player_form.html'
#    def insert_player(self, form, Players):
#        p_name = form.cleaned_data.get('player_name')
#        team_id = form.cleaned_data.get('team_id')
#        season_id = form.cleaned_data.get('season_id')
#        player_id = form.cleaned_data.get('player_id')
#        new_points = form.cleaned_data.get('points')
#        objs = Players.objects.raw('INSERT INTO DBPlayers (player_id, season_id, team_id, points, player_name) VALUES (%s, %s, %s, %s, %s)', [player_id, season_id, team_id, new_points, p_name])
#        objs.save()
#        return super().insert_player(form, Players)
    def get_success_url(self):
        return self.request.path
#
    def form_valid(self, form):
#        print(form)
        print(form.cleaned_data.get('player_name'))
        form.save()
        return super().form_valid(form)

class StatsResultView(ListView):
    model = Stats
    template_name = 'stats_page.html'

    def getStats(request, pk, tk, sk):
        if request.method == 'GET':
            object_list = Stats.objects.raw('SELECT * FROM Stats WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, tk, sk])
            return object_list

#     def get_queryset(self, pk, sk, tk):
#         # queryset = City.objects.filter(name__icontains='Boston') # new
#         query = self.request.GET.get('q')
#         if len(query) == 0:
#             object_list = Players.objects.raw('SELECT * FROM Player')
#         else:
#             object_list = Players.objects.raw('SELECT * FROM Player JOIN Teams ON Player.team_id = Teams.id WHERE player_name LIKE %s', ['%'+query+'%'])
#
# #        object_list = Players.objects.filter(
# #            Q(player_name__icontains=query)
# #        )
#         return object_list

def getUserStats1(request, pk, sk):
    player_name = Players.objects.raw('SELECT * FROM Player WHERE player_id = %s', [pk])[0]
    object_list = User2Stats.objects.raw('SELECT * FROM user1stats WHERE id = %s', [sk])
    # print(object_list)
    context = {'object_list':object_list, 'player_name':player_name}
    return render(request, 'user_stats_page.html', context)

def getUserStats2(request, pk, sk):
    player_name = Players.objects.raw('SELECT * FROM Player WHERE player_id = %s', [pk])[0]
    object_list = User2Stats.objects.raw('SELECT * FROM user2stats WHERE id = %s', [sk])
    # print(object_list)
    context = {'object_list':object_list, 'player_name':player_name}
    return render(request, 'user_stats_page.html', context)

def getStats(request, pk, tk, sk):
    player_name = Players.objects.raw('SELECT * FROM Player WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
    object_list = Stats.objects.raw('SELECT * FROM Stats WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])
    # print(object_list)
    context = {'object_list':object_list, 'player_name':player_name}
    return render(request, 'stats_page.html', context)

def createPlayer(request):
    form = PlayersForm()
    if request.method == 'POST':

        form = PlayersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
    context = {'form':form}
    return render(request, 'player_form.html', context)

#------------------------------------------PLAYER 1--------------------------------------------


# def addPlayer(request, pk, sk, tk):
#     player = Players.objects.raw('SELECT * FROM Player WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
#     if request.method == 'GET':
#         player_id = getattr(player, 'player_id')
#         season_id = getattr(player, 'season_id')
#         team_id = getattr(player, 'team_id')
#         player_name = getattr(player, 'player_name')
#         points = getattr(player, 'points')
#         index = UserPlayers.objects.count() + 1
#         # print(field_value)
#         # UserPlayers.objects.raw('INSERT INTO UserPlayers (player_id, season_id, team_id, player_name, points) VALUES (%s, %s, %s, %s, %s)', [player])
#         new = UserPlayers.objects.create(pk=index)
#         new.player_id = player_id
#         new.season_id = season_id
#         new.team_id = team_id
#         new.player_name = player_name
#         new.points = points
#         new.save()
#         return redirect('/home')
#         # form = PlayersForm(request.POST)
#         # pk = form['player_id'].value()
#         # curr_player = Players.objects.get(player_id=pk)
#         # update_form = PlayersForm(instance=curr_player)
#         # form = PlayersForm(request.POST, instance=player)
#         #
#         # # player_id = form.cleaned_data.get('player_id')
#         # # order = Player.objects.get(id=player_id)
#         # # form = PlayersForm(request.POST, instance=order)
#         # if form.is_valid():
#         #     form.save()
#     return render(request, 'home.html')

def addPlayer(request, pk, sk, tk):
    player = Players.objects.raw('SELECT * FROM Player WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
    object_list = Stats.objects.raw('SELECT * FROM Stats WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
    if request.method == 'GET':
        league_id = getattr(object_list, 'league_id')
        team_abbr = getattr(object_list, 'team_abbr')
        age = getattr(object_list, 'age')
        gp= getattr(object_list, 'gp')
        gs = getattr(object_list, 'gs')
        min = getattr(object_list, 'min')
        fgm = getattr(object_list, 'fgm')
        fga = getattr(object_list, 'fga')
        fg_pct = getattr(object_list, 'fg_pct')
        fg3m = getattr(object_list, 'fg3m')
        fg3a = getattr(object_list, 'fg3a')
        fg3_pct = getattr(object_list, 'fg3_pct')
        print(fg3_pct)
        ftm = getattr(object_list, 'ftm')
        fta = getattr(object_list, 'fta')
        ft_pct = getattr(object_list, 'ft_pct')
        oreb = getattr(object_list, 'oreb')
        dreb = getattr(object_list, 'dreb')
        reb = getattr(object_list, 'reb')
        ast = getattr(object_list, 'ast')
        stl = getattr(object_list, 'stl')
        blk = getattr(object_list, 'blk')
        tov = getattr(object_list, 'tov')
        pf = getattr(object_list, 'pf')
        pts = getattr(object_list, 'pts')
        player_id = getattr(player, 'player_id')
        season_id = getattr(player, 'season_id')
        team_id = getattr(player, 'team_id')
        player_name = getattr(player, 'player_name')
        points = getattr(player, 'points')
        index = User1Stats.objects.count() + 1
        # print(field_value)
        # UserPlayers.objects.raw('INSERT INTO UserPlayers (player_id, season_id, team_id, player_name, points) VALUES (%s, %s, %s, %s, %s)', [player])
        new = User1Stats.objects.create(pk=index)
        new.player_id = player_id
        new.player_name = player_name
        new.season_id = season_id
        new.league_id = league_id
        new.team_id = team_id
        new.team_abbr = team_abbr
        new.age = age
        new.gp = gp
        new.gs = gs
        new.min = min
        new.fgm = fgm
        new.fga = fga
        new.fg_pct = fg_pct
        new.fg3m = fg3m
        new.fg3a = fg3a
        new.fg3_pct = fg3_pct
        new.ftm = ftm
        new.fta = fta
        new.ft_pct = ft_pct
        new.oreb = oreb
        new.dreb = dreb
        new.reb = reb
        new.ast = ast
        new.stl = stl
        new.blk = blk
        new.tov = tov
        new.pf = pf
        new.pts = pts
        new.save()
        return redirect('/home')
        # form = PlayersForm(request.POST)
        # pk = form['player_id'].value()
        # curr_player = Players.objects.get(player_id=pk)
        # update_form = PlayersForm(instance=curr_player)
        # form = PlayersForm(request.POST, instance=player)
        #
        # # player_id = form.cleaned_data.get('player_id')
        # # order = Player.objects.get(id=player_id)
        # # form = PlayersForm(request.POST, instance=order)
        # if form.is_valid():
        #     form.save()
    return render(request, 'home.html')


#------------------------------------------PLAYER 2--------------------------------------------


def addPlayer2(request, pk, sk, tk):
    player = Players.objects.raw('SELECT * FROM Player WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
    object_list = Stats.objects.raw('SELECT * FROM Stats WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
    if request.method == 'GET':
        league_id = getattr(object_list, 'league_id')
        team_abbr = getattr(object_list, 'team_abbr')
        age = getattr(object_list, 'age')
        gp= getattr(object_list, 'gp')
        gs = getattr(object_list, 'gs')
        min = getattr(object_list, 'min')
        fgm = getattr(object_list, 'fgm')
        fga = getattr(object_list, 'fga')
        fg_pct = getattr(object_list, 'fg_pct')
        fg3m = getattr(object_list, 'fg3m')
        fg3a = getattr(object_list, 'fg3a')
        fg3_pct = getattr(object_list, 'fg3_pct')
        ftm = getattr(object_list, 'ftm')
        fta = getattr(object_list, 'fta')
        ft_pct = getattr(object_list, 'ft_pct')
        oreb = getattr(object_list, 'oreb')
        dreb = getattr(object_list, 'dreb')
        reb = getattr(object_list, 'reb')
        ast = getattr(object_list, 'ast')
        stl = getattr(object_list, 'stl')
        blk = getattr(object_list, 'blk')
        tov = getattr(object_list, 'tov')
        pf = getattr(object_list, 'pf')
        pts = getattr(object_list, 'pts')
        player_id = getattr(player, 'player_id')
        season_id = getattr(player, 'season_id')
        team_id = getattr(player, 'team_id')
        player_name = getattr(player, 'player_name')
        points = getattr(player, 'points')
        index = User2Stats.objects.count() + 1
        # print(field_value)
        # UserPlayers.objects.raw('INSERT INTO UserPlayers (player_id, season_id, team_id, player_name, points) VALUES (%s, %s, %s, %s, %s)', [player])
        new = User2Stats.objects.create(pk=index)
        new.player_id = player_id
        new.player_name = player_name
        new.season_id = season_id
        new.league_id = league_id
        new.team_id = team_id
        new.team_abbr = team_abbr
        new.age = age
        new.gp = gp
        new.gs = gs
        new.min = min
        new.fgm = fgm
        new.fga = fga
        new.fg_pct = fg_pct
        new.fg3m = fg3m
        new.fg3a = fg3a
        new.fg3_pct = fg3_pct
        new.ftm = ftm
        new.fta = fta
        new.ft_pct = ft_pct
        new.oreb = oreb
        new.dreb = dreb
        new.reb = reb
        new.ast = ast
        new.stl = stl
        new.blk = blk
        new.tov = tov
        new.pf = pf
        new.pts = pts
        new.save()
        return redirect('/home')
        # form = PlayersForm(request.POST)
        # pk = form['player_id'].value()
        # curr_player = Players.objects.get(player_id=pk)
        # update_form = PlayersForm(instance=curr_player)
        # form = PlayersForm(request.POST, instance=player)
        #
        # # player_id = form.cleaned_data.get('player_id')
        # # order = Player.objects.get(id=player_id)
        # # form = PlayersForm(request.POST, instance=order)
        # if form.is_valid():
        #     form.save()
    return render(request, 'home.html')


def updatePlayer(request, pk, sk, tk):
    # player_stats = Stats.objects.raw('SELECT * FROM Stats WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
    player = Players.objects.raw('SELECT * FROM Player WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
    form = PlayersForm(instance=player)
    if request.method == 'POST':
        # form = PlayersForm(request.POST)
        # pk = form['player_id'].value()
        # curr_player = Players.objects.get(player_id=pk)
        # update_form = PlayersForm(instance=curr_player)
        form = PlayersForm(request.POST, instance=player)
        # player_id = form.cleaned_data.get('player_id')
        if form.is_valid():
            form.save()
            return redirect('/home')

    context = {'form':form}
    return render(request, 'update_form.html', context)

# def updatePlayer1(request, pk):
#     # player_stats = Stats.objects.raw('SELECT * FROM Stats WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
#     player = UserPlayers.objects.get(id=pk)
#     # player = Players.objects.raw('SELECT * FROM User WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
#     form = UserForm1(instance=player)
#     if request.method == 'POST':
#         # form = PlayersForm(request.POST)
#         # pk = form['player_id'].value()
#         # curr_player = Players.objects.get(player_id=pk)
#         # update_form = PlayersForm(instance=curr_player)
#         form = UserForm1(request.POST, instance=player)
#         # player_id = form.cleaned_data.get('player_id')
#         if form.is_valid():
#             form.save()
#             return redirect('/home')
#
#     context = {'form':form}
#     return render(request, 'update_form.html', context)

def updatePlayer1(request, pk):
    # player_stats = Stats.objects.raw('SELECT * FROM Stats WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
    player = User1Stats.objects.get(id=pk)
    # player = Players.objects.raw('SELECT * FROM User WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
    form = UserForm1(instance=player)
    if request.method == 'POST':
        # form = PlayersForm(request.POST)
        # pk = form['player_id'].value()
        # curr_player = Players.objects.get(player_id=pk)
        # update_form = PlayersForm(instance=curr_player)
        form = UserForm1(request.POST, instance=player)
        # player_id = form.cleaned_data.get('player_id')
        if form.is_valid():
            form.save()
            return redirect('/home')

    context = {'form':form}
    return render(request, 'update_form.html', context)


def updatePlayer2(request, pk):
    # player_stats = Stats.objects.raw('SELECT * FROM Stats WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
    player = User2Stats.objects.get(id=pk)
    # player = Players.objects.raw('SELECT * FROM User WHERE player_id = %s AND team_id = %s AND season_id = %s', [pk, sk, tk])[0]
    form = UserForm2(instance=player)
    if request.method == 'POST':
        # form = PlayersForm(request.POST)
        # pk = form['player_id'].value()
        # curr_player = Players.objects.get(player_id=pk)
        # update_form = PlayersForm(instance=curr_player)
        form = UserForm2(request.POST, instance=player)
        # player_id = form.cleaned_data.get('player_id')
        if form.is_valid():
            form.save()
            return redirect('/home')

    context = {'form':form}
    return render(request, 'update_form.html', context)


def deletePlayer(request, pk):
    player = Players.objects.raw('SELECT * FROM Player WHERE player_id = %s', [pk])[0]
    if request.method == 'POST':
        # form = PlayersForm(request.POST)
        # pk = form['player_id'].value()
        # curr_player = Players.objects.get(player_id=pk)
        # update_form = PlayersForm(instance=curr_player)
        # form = PlayersForm(request.POST, instance=curr_player)
        player.delete()
        return redirect('/home')
        # player_id = form.cleaned_data.get('player_id')
        # order = Player.objects.get(id=player_id)
        # form = PlayersForm(request.POST, instance=order)
        # if form.is_valid():
        #     form.delete()
        #     return redirect('/home')

    context = {'object':player}
    return render(request, 'delete_form.html', context)


# def deletePlayer1(request, pk):
#     player = UserPlayers.objects.raw('SELECT * FROM User WHERE id = %s', [pk])[0]
#     if request.method == 'POST':
#         # form = PlayersForm(request.POST)
#         # pk = form['player_id'].value()
#         # curr_player = Players.objects.get(player_id=pk)
#         # update_form = PlayersForm(instance=curr_player)
#         # form = PlayersForm(request.POST, instance=curr_player)
#         player.delete()
#         return redirect('/home')
#         # player_id = form.cleaned_data.get('player_id')
#         # order = Player.objects.get(id=player_id)
#         # form = PlayersForm(request.POST, instance=order)
#         # if form.is_valid():
#         #     form.delete()
#         #     return redirect('/home')
#
#     context = {'object':player}
#     return render(request, 'delete_form.html', context)

def deletePlayer1(request, pk):
    player = User1Stats.objects.raw('SELECT * FROM user1stats WHERE id = %s', [pk])[0]
    player_name = copy.copy(getattr(player, 'player_name'))
    if request.method == 'POST':
        # form = PlayersForm(request.POST)
        # pk = form['player_id'].value()
        # curr_player = Players.objects.get(player_id=pk)
        # update_form = PlayersForm(instance=curr_player)
        # form = PlayersForm(request.POST, instance=curr_player)
        player.delete()
        return redirect('/home')
        # player_id = form.cleaned_data.get('player_id')
        # order = Player.objects.get(id=player_id)
        # form = PlayersForm(request.POST, instance=order)
        # if form.is_valid():
        #     form.delete()
        #     return redirect('/home')

    context = {'object':player, 'name':player_name}
    return render(request, 'delete_form.html', context)

def deletePlayer2(request, pk):
    # player_name = Players.objects.raw('SELECT * FROM Player WHERE player_id = %s', [pk])
    player = User2Stats.objects.raw('SELECT * FROM user2stats WHERE id = %s', [pk])[0]
    player_name = copy.copy(getattr(player, 'player_name'))
    print(player_name)
    if request.method == 'POST':
        # form = PlayersForm(request.POST)
        # pk = form['player_id'].value()
        # curr_player = Players.objects.get(player_id=pk)
        # update_form = PlayersForm(instance=curr_player)
        # form = PlayersForm(request.POST, instance=curr_player)
        player.delete()
        return redirect('/home')
        # player_id = form.cleaned_data.get('player_id')
        # order = Player.objects.get(id=player_id)
        # form = PlayersForm(request.POST, instance=order)
        # if form.is_valid():
        #     form.delete()
        #     return redirect('/home')

    context = {'object':player, 'name':player_name}
    return render(request, 'delete_form.html', context)

# def deleteAllPlayers1(request):
#     player = UserPlayers.objects.all()
#     if request.method == 'POST':
#         player.delete()
#         return redirect('/home')
#
#     context = {'object':player}
#     return render(request, 'delete_form.html', context)


def deleteAllPlayers1(request):
    player = User1Stats.objects.all()
    if request.method == 'POST':
        player.delete()
        return redirect('/home')

    context = {'object':player}
    return render(request, 'delete_form.html', context)


def deleteAllPlayers2(request):
    player = User2Stats.objects.all()
    if request.method == 'POST':
        player.delete()
        return redirect('/home')

    context = {'object':player}
    return render(request, 'delete_form.html', context)

class PlayersDeleteView(FormView):
    form_class = DeleteForm
    template_name = 'delete_form.html'
    cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password123',
    database='NBA'
    )
    cursor = cnx.cursor()
    def delete_player(self, form, Players):
        print(form.cleaned_data())
        print("Test PRINTTTT")
        print("Logging message", flush=True)
        p_name = form.cleaned_data.get('player_name')
        team_id = form.cleaned_data.get('team_id')
        season_id = form.cleaned_data.get('season_id')
        player_id = form.cleaned_data.get('player_id')
        new_points = form.cleaned_data.get('points')
        objs = Players.objects.get(player_id=player_id, season_id=season_id, team_id=team_id).delete()
        Players.objects.all.save()
        SQLFormula = 'DELETE DBPlayers WHERE player_id = %s AND season_id = %s AND team_id = %s)'
        cursor.execute(SQLFormula, [player_id, season_id, team_id])
        cnx.commit()
        return super().delete_player(form)
    def get_success_url(self):
        return self.request.path

#    def valid_update(self, form):
#        form.save()
##        print(object_list)
###        object_list.points = new_points
##        object_list.save()
##        print(object_list)
##        object_list[0][0] = points
##        object_list[0].save()
#        return super().valid_update(form)

# class PlayersUpdateView(FormView):
#     form_class = UpdateForm
#     template_name = 'update_form.html'
#     cnx = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     passwd='password123',
#     database='NBA'
#     )
#     cursor = cnx.cursor()
#     def insert_player(self, form, Players):
#         print(form.cleaned_data())
#         print("PRINTTTT")
#         print("Logging message", flush=True)
#         p_name = form.cleaned_data.get('player_name')
#         team_id = form.cleaned_data.get('team_id')
#         season_id = form.cleaned_data.get('season_id')
#         player_id = form.cleaned_data.get('player_id')
#         new_points = form.cleaned_data.get('points')
#         objs = Players.objects.get(player_id=player_id, season_id=season_id, team_id=team_id, player_name=p_name)
#         objs.points = new_points
#         objs.save()
#         SQLFormula = 'UPDATE DBPlayers SET points = %s WHERE player_id = %s AND season_id = %s AND team_id = %s AND player_name = %s)'
#         cursor.execute("UPDATE DBPlayers SET points='"+new_points+"'WHERE player_id = '"+player_id+"'")
#         cnx.commit()
#         return render(get_success_url())
#     def get_success_url(self):
#         return self.request.path
#
#     def valid_update(self, form):
#         form.save()
# #        print(object_list)
# ##        object_list.points = new_points
# #        object_list.save()
# #        print(object_list)
# #        object_list[0][0] = points
# #        object_list[0].save()
#         return super().valid_update(form)
#        print(object_list[0])
# class SearchResultsView(ListView):
#     model = Players
#     template_name = 'search_results.html'
# cities/views.py
class SearchResultsView(ListView):
    model = Players
    template_name = 'search_results.html'

    def get_queryset(self):
        # queryset = City.objects.filter(name__icontains='Boston') # new
        query = self.request.GET.get('q')
        if len(query) == 0:
            object_list = Players.objects.raw('SELECT * FROM Player')
        else:
            object_list = Players.objects.raw('SELECT * FROM Player JOIN Teams ON Player.team_id = Teams.id WHERE player_name LIKE %s', ['%'+query+'%'])



#        object_list = Players.objects.filter(
#            Q(player_name__icontains=query)
#        )
        return object_list

def gameSimulator(request):
    players = User1Stats.objects.all()
    team1_sz = User1Stats.objects.all().count()
    team2_sz = User2Stats.objects.all().count()
    team1 = np.full((13, team1_sz), 0.0)
    team2 = np.full((13, team2_sz), 0.0)
    for i, player in enumerate(players):
        player_id = getattr(player, 'player_id')
        season_id = getattr(player, 'season_id')
        team_id = getattr(player, 'team_id')
        object_list = Stats.objects.raw('SELECT * FROM user1stats JOIN Teams ON user1stats.team_id = Teams.id WHERE player_id = %s AND team_id = %s AND season_id = %s', [player_id, team_id, season_id])[0]
        team1[0, i] += getattr(object_list, 'gp')
        team1[1, i] += float(getattr(object_list, 'fg_pct'))
        team1[2, i] += float(getattr(object_list, 'fg3_pct'))
        team1[3, i] += float(getattr(object_list, 'ft_pct'))
        team1[4, i] += getattr(object_list, 'oreb')
        team1[5, i] += getattr(object_list, 'dreb')
        team1[6, i] += getattr(object_list, 'reb')
        team1[7, i] += getattr(object_list, 'ast')
        team1[8, i] += getattr(object_list, 'stl')
        team1[9, i] += getattr(object_list, 'blk')
        team1[10, i] += getattr(object_list, 'tov')
        team1[11, i] += getattr(object_list, 'pf')
        team1[12, i] += getattr(object_list, 'pts')
    opponents = User2Stats.objects.all()
    for i, player in enumerate(opponents):
        player_id = getattr(player, 'player_id')
        season_id = getattr(player, 'season_id')
        team_id = getattr(player, 'team_id')
        object_list = Stats.objects.raw('SELECT * FROM user2stats JOIN Teams ON user2stats.team_id = Teams.id WHERE player_id = %s AND team_id = %s AND season_id = %s', [player_id, team_id, season_id])[0]
        team2[0, i] += getattr(object_list, 'gp')
        team2[1, i] += float(getattr(object_list, 'fg_pct'))
        team2[2, i] += float(getattr(object_list, 'fg3_pct'))
        team2[3, i] += float(getattr(object_list, 'ft_pct'))
        team2[4, i] += getattr(object_list, 'oreb')
        team2[5, i] += getattr(object_list, 'dreb')
        team2[6, i] += getattr(object_list, 'reb')
        team2[7, i] += getattr(object_list, 'ast')
        team2[8, i] += getattr(object_list, 'stl')
        team2[9, i] += getattr(object_list, 'blk')
        team2[10, i] += getattr(object_list, 'tov')
        team2[11, i] += getattr(object_list, 'pf')
        team2[12, i] += getattr(object_list, 'pts')
    team1_win, team2_win, tie = gamesSim(team1, team2, 500)
    # print(team2)


    context = {'players':players, 'opponents':opponents, 'team1':team1_win, 'team2':team2_win, 'tie':tie}
    return render(request, 'simulator.html', context)


def gameSim(team1, team2):
    # rnd.seed(j)
    size = len(team1)
    # print(size)
    T1 = 0
    T2 = 0
    for i in range(0, size):
        # rnd.seed(j*i)
        T1 += rnd.gauss(np.mean(team1[i]), np.std(team1[i]))
        # rnd.seed(j*(i+i))
        T2 += rnd.gauss(np.mean(team2[i]), np.std(team2[i]))
    T1 /= 13
    T2 /= 13
    if len(team1[0]) < len(team2[0]):
        T1 /= (len(team2[0]) / len(team1[0]))
        T2 *= (len(team2[0]) / len(team1[0]))
    elif len(team1[0]) > len(team2[0]):
        T1 *= (len(team1[0]) / len(team2[0]))
        T2 /= (len(team1[0]) / len(team2[0]))
    print(T1, T2)
    if abs(T1 - T2) < 10:
        return 0
    elif T1 > T2:
        return 1
    elif T1 < T2:
        return -1
    else:
        return 0

def gamesSim(team1, team2, num_sims):
    team1win = 0
    team2win = 0
    tie = 0
    for i in range(num_sims):
        #calls the pervious game simulator and aggregates results
        gm = gameSim(team1, team2)
        if gm == 1:
            team1win +=1
        elif gm == -1:
            team2win +=1
        else: tie +=1
    team1_pct = 'Team 1 Win Percentage: ' + str(team1win/(team1win+team2win+tie))
    team2_pct = 'Team 2 Win Percentage: ' + str(team2win/(team1win+team2win+tie))
    tie = 'Tie Percentage: ' + str(tie/(team1win+team2win+tie))

    return team1_pct, team2_pct, tie
    #can see all results using self.results


class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


def getSeasons(request, pk):
    object_list = Players.objects.raw('SELECT * FROM Player JOIN Teams ON Player.team_id = Teams.id WHERE player_id = %s', [pk])
    context = {'object_list':object_list}
    return render(request, 'search_results.html', context)


def viewTeammates(request, pk, sk, tk):
    # players = Players.objects.all()
    print('YO')
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="password123")
    print('YO')
    s = '''
                    MATCH (a:Player)-[r:TEAMMATES_WITH]->(b:Player)
                    WHERE a.playerID = {0} AND a.seasonID = '{1}'
                    RETURN b
                    '''
    query_string = s.format(pk, sk)
    print(query_string)
    list = []
    result = conn.query(query_string)
    for node in result:
        list.append(node['b']['playerName'])
        # print('YO')
    in_list = '('
    for i, player in enumerate(list):
        if i == (len(list) - 1):
            in_list += str(player)
        else:
            in_list += str(player)
            in_list += ', '
    in_list += ')'

    # print(in_list)

    # object_list = Players.objects.raw('SELECT * FROM Player WHERE player_id IN %s', in_list)
    object_list = Players.objects.filter(player_name__in=list, season_id=sk, team_id=tk)
    team_name = Teams.objects.raw('SELECT * FROM Teams WHERE id = %s', [tk])[0]
    print(getattr(team_name, 'team_name'))
    context = {'object_list':object_list, 'team_name':team_name}
    return render(request, 'team_mates.html', context)


# s = '''name={0},
# address={1},
# nickname={2},
# age={3},
# comments=
# """
# {4}
# """
# '''
#
# print s.format("alice", "N/A", "alice", 18, "missing person")


# def simple_upload(request):
#     if request.method == 'POST':
#         person_resource = PlayersResource()
#         dataset = Dataset()
#         new_players = request.FILES['myfile']
#
#         imported_data = dataset.load(new_players.read())
#         result = person_resource.import_data(dataset, dry_run=True)  # Test the data import
#
#         if not result.has_errors():
#             person_resource.import_data(dataset, dry_run=False)  # Actually import now
#
#     return render(request, templates/'home.html')
