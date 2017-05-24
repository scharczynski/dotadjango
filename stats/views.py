# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Team, Player
import requests


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



class IndexView(generic.ListView):
    template_name = 'stats/index.html'
    context_object_name = 'teams'
    
    

    def get_queryset(self):
        """Return the last five published questions."""
        return Team.objects.all()

    print Team.objects.all()

# class TeamView(generic.DetailView):
#     model = Team
#     template_name = 'stats/team.html'
    
def match(request):
    match = requests.get('https://api.opendota.com/api/matches/3200576427')
    return render(request, 'stats/match.html', {'match':match})


# class PlayerView(generic.DetailView):
#     model = Player
#     template_name = 'stats/player.html'

def teams(request):
    teams = Team.objects.all()

    return render(request,'stats/teams.html', {'teams':teams})
    #template_name = 'stats/teams.html'
    #context_object_name = 'teams'
