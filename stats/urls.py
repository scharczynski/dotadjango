from django.conf.urls import url

from . import views

app_name = 'stats'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    
    # ex: /polls/5/
    url(r'teams/(?P<team_id>[0-9]+)/$', views.team, name='team'),
    url(r'teams$', views.teams, name='teams'),
    # ex: /polls/5/results/
    url(r'^player/(?P<player_id>[0-9]+)/$', views.player, name='player'),

    url(r'^match', views.match, name='match'),
    url(r'^lookup/(?P<steam_id>[0-9]+)/$', views.lookup, name='lookup'),
    # ex: /polls/5/vote/
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]