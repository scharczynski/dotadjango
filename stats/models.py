# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=200)

    def __str__(self):
        return self.team_name
    


class Player(models.Model):
    player_name = models.CharField(max_length=200)
    steam_id = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.player_name



# class Teams(models.Model):
#     teams = 

#     def __str__(self):
#         return str(team.team_name for team in teams)