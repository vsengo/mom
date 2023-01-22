from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import re_path
from .views import runAddView, runListView, runDelView, runUpdView
from .views import xtrainAddView, xtrainDelView, xtrainListView, xtrainUpdView
from .views import runWeekAddView, runWeekDelView, runWeekListView, runWeekUpdView, runScheduleView
from .views import halfMarathonAddView, halfMarathonDelView, halfMarathonListView, halfMarathonUpdView

urlpatterns = [
    re_path(r'runList', runListView, name='runList'),
    re_path(r'runAdd',  runAddView,  name='runAdd'),
    re_path(r'runDel(?P<pk>\d+)', runDelView, name='runDel'),
    re_path(r'runUpd(?P<pk>\d+)', runUpdView,  name='runUpd'),
    re_path(r'xtrainList', xtrainListView, name='xtrainList'),
    re_path(r'xtrainAdd', xtrainAddView,  name='xtrainAdd'),
    re_path(r'xtrainDel(?P<pk>\d+)', xtrainDelView, name='xtrainDel'),
    re_path(r'xtrainUpd(?P<pk>\d+)', xtrainUpdView,  name='xtrainUpd'),
    re_path(r'runWeekList', runWeekListView, name='runWeekList'),
    re_path(r'runWeekAdd', runWeekAddView,  name='runWeekAdd'),
    re_path(r'runWeekDel(?P<pk>\d+)', runWeekDelView, name='runWeekDel'),
    re_path(r'runWeekUpd(?P<pk>\d+)', runWeekUpdView,  name='runWeekUpd'),
    re_path(r'raceSchedule(?P<pk>\d+)', runScheduleView,  name='runSchedule'),
    re_path(r'halfMarathonList', halfMarathonListView, name='halfMarathonList'),
    re_path(r'raceAdd', halfMarathonAddView,  name='raceAdd'),
    re_path(r'halfMarathonDel(?P<pk>\d+)', halfMarathonDelView, name='halfMarathonDel'),
    re_path(r'halfMarathonUpd(?P<pk>\d+)', halfMarathonUpdView,  name='halfMarathonUpd'),
]
    