from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import re_path
from .views import activityAddView, activityListView, activityDelView, activityUpdView
from .views import weeklyActivityAddView, weeklyActivityDelView, weeklyActivityListView, weeklyActivityUpdView
from .views import halfMarathonAddView, halfMarathonDelView, halfMarathonListView, halfMarathonUpdView, trainingView, runWeekView

urlpatterns = [
    re_path(r'activityList', activityListView, name='activityList'),
    re_path(r'activityAdd',  activityAddView,  name='activityAdd'),
    re_path(r'activityDel(?P<pk>\d+)', activityDelView, name='activityDel'),
    re_path(r'activityUpd(?P<pk>\d+)', activityUpdView,  name='activityUpd'),
    re_path(r'weeklyActivityList', weeklyActivityListView, name='weeklyActivityList'),
    re_path(r'weklyActivityAdd', weeklyActivityAddView,  name='weeklyActivityAdd'),
    re_path(r'weeklyActivityDel(?P<pk>\d+)', weeklyActivityDelView, name='weeklyActivityDel'),
    re_path(r'weeklyActivityUpd(?P<pk>\d+)', weeklyActivityUpdView,  name='weeklyActivityUpd'),
    re_path(r'trainingList(?P<pk>\d+)', trainingView,  name='trainingList'),
    re_path(r'runweekList(?P<pk>\d+)', runWeekView,  name='runweekList'),
    re_path(r'halfMarathonList', halfMarathonListView, name='halfMarathonList'),
    re_path(r'raceAdd', halfMarathonAddView,  name='raceAdd'), 
    re_path(r'halfMarathonDel(?P<pk>\d+)', halfMarathonDelView, name='halfMarathonDel'),
    re_path(r'halfMarathonUpd(?P<pk>\d+)', halfMarathonUpdView,  name='halfMarathonUpd'),
]