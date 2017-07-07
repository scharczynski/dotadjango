# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Team, Player
import requests
import json
from .forms import IdForm

# def index(request):
#     teams = Team.objects.all()
#     players = [p.player_name for p in Player.objects.all()]
#     #return HttpResponse(teams[0].team_name + ": " + out)
#     #return HttpResponse(players)

#     context = {'teams': teams, 'players':players}
#     return render(request, 'stats/index.html', context)

def team(request, team_id):
    
    team = get_object_or_404(Team, pk=team_id)
    players = team.player_set.all()

    return render(request, 'stats/team.html', {'team': team, 'players':players})
    #return HttpResponse("You're looking at team %s." % team_id)

def player(request, player_id):
    player = get_object_or_404(Player, pk = player_id)
    return render(request ,'stats/player.html', {'player':player})



# class TeamView(generic.DetailView):
#     model = Team
#     template_name = 'stats/team.html'
    
def match(request):
    match = requests.get('https://api.opendota.com/api/matches/3200576427')
    return render(request, 'stats/match.html', {'match':match})


# class PlayerView(generic.DetailView):
#     model = Player
#     template_name = 'stats/player.html'

def index(request):
    if request.method == 'POST':
            # create a form instance and populate it with data from the request:
        form = IdForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = IdForm()

    return render(request, 'stats/index.html', {'form': form})
    

def teams(request):
    teams = Team.objects.all()

    return render(request,'stats/teams.html', {'teams':teams})
    #template_name = 'stats/teams.html'
    #context_object_name = 'teams'

def results(request):
    print request.POST['steam_id']
    steam_id = request.POST['steam_id']
    player_heroes = requests.get('https://api.opendota.com/api/players/'+str(steam_id)+'/heroes?limit=1000')
    hero_info = requests.get('https://api.opendota.com/api/heroStats')
    player = requests.get('https://api.opendota.com/api/players/'+str(steam_id))
    parsed_player = player.json()
    parsed_player_heroes = player_heroes.json()
    parsed_hero_info = hero_info.json()
    hero_wins = []
    namelist = {}
    fivek_winrate = []
    fivek_dict = {}
    top_compares = []
    comparedict = {}

   

    for j in parsed_hero_info:
        namelist[j["id"]]  =  j["localized_name"]
        fivewin = float(j['5000_win']) / j['5000_pick']
        fivek_dict[j["id"]] = fivewin

    for i in parsed_player_heroes:
        if i['games'] != 0:
            player_winrate = float(i['win']) / i['games']
        else:
            player_winrate = 0
        #print i['win'] / i['games']
        #rint i['games']
        hero_id = int(i["hero_id"])
        compare_winrate = player_winrate / fivek_dict[hero_id]
        hero_wins.append((player_winrate, namelist[int(hero_id)], compare_winrate))
        comparedict[hero_id] = compare_winrate
        top_compares.append((compare_winrate, namelist[int(hero_id)], i['games']))
        

    solo_mmr = parsed_player['solo_competitive_rank']
    profile = parsed_player['profile']
    name = profile['name']
    persona_name = profile['personaname']


    top_compares.sort()
    
    #print top_compares[0][3]
    filtered_compares = list(filter(lambda x: x[2] > 10, top_compares))
    filtered_compares.sort(key=lambda x: x[0], reverse=True)
    print filtered_compares
    print len(top_compares)
    print len(filtered_compares)
    #print comparedict

    return render(request, 'stats/results.html', {'player':player, 'solo_mmr': solo_mmr, 'name':name, 'persona_name':persona_name, 'top3':hero_wins[:3], 'top3_relative': filtered_compares[:5]})

def lookup(request, steam_id):
    player = requests.get('https://api.opendota.com/api/players/'+str(steam_id))
    heroes = requests.get('https://api.opendota.com/api/players/'+str(steam_id)+'/heroes')
    hero_stats = requests.get('https://api.opendota.com/api/heroStats')
    parsed_heroes = heroes.json()
    parsed_player = player.json()
    parsed_hero_stats= hero_stats.json()
    hero_wins = []
    namelist = {}
    fivek_winrate = []
    fivek_dict = {}
    top_compares = []
    comparedict = {}

   

    for j in parsed_hero_stats:
        namelist[j["id"]]  =  j["localized_name"]
        fivewin = float(j['5000_win']) / j['5000_pick']
        fivek_dict[j["id"]] = fivewin

    for i in parsed_heroes:
        player_winrate = float(i['win']) / i['games']
        #print i['win'] / i['games']
        #rint i['games']
        hero_id = int(i["hero_id"])
        compare_winrate = player_winrate / fivek_dict[hero_id]
        hero_wins.append((player_winrate, namelist[int(hero_id)], compare_winrate))
        comparedict[hero_id] = compare_winrate
        top_compares.append(compare_winrate)
        

    solo_mmr = parsed_player['solo_competitive_rank']
    profile = parsed_player['profile']
    name = profile['name']
    persona_name = profile['personaname']

    top_compares.sort()




    return render(request, 'stats/lookup.html', {'player':player, 'solo_mmr': solo_mmr, 'name':name, 'persona_name':persona_name, 'top3':hero_wins[:3], 'top3_relative': top_compares[:-3]})