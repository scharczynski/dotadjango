# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Team, Player, Hero 

# Register your models here.
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Hero)