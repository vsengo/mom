from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template  import loader
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView
from django.contrib  import messages
from django.db import IntegrityError
from .models import Activity, WeeklyActivity, Race, Training
from .forms import ActivityForm, WeeklyActivityForm, RaceForm
from util.date import DateUtil

def getUserRole(user):
    return 'EDIT'

@login_required
def activityAddView(request):
    return activityUpdView(request,'x')

@login_required
def activityUpdView(request,pk):
    if request.method == 'GET':
        if pk=='x':
            form = ActivityForm()
            run = Activity()
        else:
            run = Activity.objects.get(id=pk) 

        form  = ActivityForm(instance = run)
        form_name="Activity"
        return render(request,template_name='common_form.html',context={'form':form, 'form_name':form_name})

    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            if pk != 'x':
                obj.id=pk
            obj.save()
            print("Saved "+str(pk))
        else:
            error={'message':'Error in Data input to Run'}
            return render(request,template_name='error.html',context=error)

        return redirect('training:activityList')

@login_required
def activityListView(request):
    if request.method == 'GET':
        runs = Activity.objects.all()
        userRole = getUserRole(request.user)
        return render(request = request,template_name = "run_list.html",context={'run_list':runs, 'userRole':userRole})

 
@login_required
def activityDelView(request,pk):
    run = Activity.objects.get(id=pk)
    run.delete()        
    return redirect('training:activityList')

@login_required
def weeklyActivityAddView(request):
    return weeklyActivityUpdView(request,'x')

@login_required
def weeklyActivityUpdView(request,pk):
    if request.method == 'GET':
        if pk=='x':
            form = WeeklyActivityForm()
            run = WeeklyActivity()
        else:
            run = WeeklyActivity.objects.get(id=pk) 

        form  = WeeklyActivityForm(instance = run)
        form_name="WeeklyActivity"
        return render(request,template_name='common_form.html',context={'form':form, 'form_name':form_name})

    if request.method == 'POST':
        form = WeeklyActivityForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            if pk != 'x':
                obj.id=pk
            obj.save()

            print("Saved "+str(pk))
        else:
            error={'message':'Error in Data input to Run'}
            return render(request,template_name='error.html',context=error)

        return redirect('training:weeklyActivityList')

@login_required
def weeklyActivityListView(request):
    if request.method == 'GET':
        data = WeeklyActivity.objects.all()
        userRole = getUserRole(request.user)
        return render(request = request,template_name = "WeeklyActivity_list.html",context={'data_list':data, 'userRole':userRole})

@login_required
def weeklyActivityDelView(request,pk):
    data = WeeklyActivity.objects.get(id=pk)
    data.delete()        
    return redirect('training:weeklyActivityList')

def trainingView(request,pk):
    if request.method == 'GET':
       
        data = Training.objects.filter(race_id=pk)

        weeks = []
        for row in data:
            weeks.append(row.weeks_id)
            numWeeks  = row.numberOfWeeks

        data = WeeklyActivity.objects.filter(id__in=weeks)

        race = Race.objects.get(id=pk)
        wk=DateUtil.dateWeekStarting(race.start)
        userRole = 'VIEW'
        context={
            'data_list':data,
            'race':race,
            'numWeeks':numWeeks,
            'week_start':wk,
            'userRole':userRole,
        }
        return render(request = request,template_name = "train_list.html",context=context)

def runWeekView(request,pk):
    if request.method == 'GET':
        race = Race.objects.get(id=pk)
        weekDate, nWeek=DateUtil.dateWeekStarting(race.start)
       
        data = Training.objects.filter(race_id=pk)

        row = data[nWeek].weeks
        numWeeks = data[nWeek].numberOfWeeks
        data_list=[]
        data_list.append(row.monday)
        data_list.append(row.tuesday)
        data_list.append(row.wednesday)
        data_list.append(row.thursday)
        data_list.append(row.friday)
        data_list.append(row.saturday)
        data_list.append(row.sunday)
        
        userRole = 'VIEW'
        context={
            'data_list':data_list,
            'race':race,
            'numWeeks':numWeeks,
            'week_start':weekDate,
            'userRole':userRole,
        }
        return render(request = request,template_name = "runweek.html",context=context)

@login_required
def halfMarathonAddView(request):
    return halfMarathonUpdView(request,'x')

@login_required
def halfMarathonUpdView(request,pk):
    if request.method == 'GET':
        if pk=='x':
            form = RaceForm()
            run = Race()
        else:
            run = Race.objects.get(id=pk) 

        form  = RaceForm(instance = run)
        form_name="HalfMarathon"
        return render(request,template_name='common_form.html',context={'form':form, 'form_name':form_name})

    if request.method == 'POST':
        form = RaceForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            if pk != 'x':
                obj.id=pk
            obj.save()
        else:
            error={'message':'Error in Data input to Run'}
            return render(request,template_name='error.html',context=error)

        return redirect('training:halfMarathonList')

@login_required
def halfMarathonListView(request):
    if request.method == 'GET':
        data = Race.objects.all()
        userRole = getUserRole(request.user)
        return render(request = request,template_name = "race_list.html",context={'data_list':data, 'userRole':userRole})

@login_required
def halfMarathonDelView(request,pk):
    data = Race.objects.get(id=pk)
    data.delete()        
    return redirect('training:halfMarathonList')