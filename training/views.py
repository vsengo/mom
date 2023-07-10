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
from .models import Activity, WeeklyActivity, Race, Training, UserRace
from .forms import ActivityForm, WeeklyActivityForm, RaceForm, UserRaceForm
from util.date import DateUtil
from datetime import timedelta

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
            total = 0
            if obj.monday.type == 'RUN':
                total += obj.monday.minutes
            if obj.tuesday.type == 'RUN':
                total += obj.tuesday.minutes
            if obj.wednesday.type == 'RUN':
                total += obj.wednesday.minutes
            if obj.thursday.type == 'RUN':
                total += obj.thursday.minutes
            if obj.friday.type == 'RUN':
                total += obj.friday.minutes
            if obj.saturday.type == 'RUN':
                total += obj.saturday.minutes
            if obj.sunday.type == 'RUN':
                total += obj.sunday.minutes
            obj.total = total
            obj.save()
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
        racePace=10

        if request.user.id != None:
            userRace = UserRace.objects.all().filter(user=request.user).filter(race_id=pk)
            if userRace:
                racePace=userRace.first().easyPace
               
        weekDate, nWeek=DateUtil.dateWeekStarting(race.end)
       
        data = Training.objects.filter(race_id=pk)
        trainWeek=0
        if nWeek < data[0].numberOfWeeks:
            trainWeek = data[0].numberOfWeeks - nWeek
    

        row = data[trainWeek].weeks
        data_list=[]
        data_list.append(row.monday)
        data_list.append(row.tuesday)
        data_list.append(row.wednesday)
        data_list.append(row.thursday)
        data_list.append(row.friday)
        data_list.append(row.saturday)
        data_list.append(row.sunday)
        
        long_run = row.saturday.minutes
        long_distance= int(long_run/racePace)
        total_distance = int(row.total/racePace)
        userRole = 'VIEW'
        context={
            'data_list':data_list,
            'race':race,
            'numWeeks':trainWeek + 1,
            'week_start':weekDate,
            'userRole':userRole,
            'total' : total_distance,
            'long_run' : long_distance,
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

@login_required
def userRaceAddView(request):
    return userRaceUpdView(request,'x')

@login_required
def userRaceUpdView(request,pk):
    if request.method == 'GET':
        if pk=='x':
            form = UserRaceForm()
            race = UserRace()
        else:
            race = UserRace.objects.get(id=pk) 

        form  = UserRaceForm(instance = race)
        form_name="UserRace"
        return render(request,template_name='common_form.html',context={'form':form, 'form_name':form_name})

    if request.method == 'POST':
        form = UserRaceForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            if pk != 'x':
                obj.id=pk
            
            obj.user=request.user
            avgPace=float(obj.targetTimeInMin/obj.race.distance)
            obj.longPace=obj.easyPace=avgPace + 1
            obj.tempoPace=avgPace - 1
            obj.vo2Pace = avgPace - 1.25
            obj.speedPace = avgPace - 1.5
            obj.avgPace = avgPace
            obj.save()

            print("Saved User Race "+str(pk))
        else:
            error={'message':'Error in Data input to Run'}
            return render(request,template_name='error.html',context=error)

        return redirect('training:activityList')
    
@login_required
def userRaceDelView(request,pk):
    data = UserRace.objects.get(id=pk)
    data.delete()        
    return redirect('training:activityList')

@login_required
def userRaceListView(request):
    if request.method == 'GET':
        data = UserRace.objects.all().filter(user=request.user)
        userRole = getUserRole(request.user)
        if not data:
            return redirect('training:userRaceAdd')
        else:   
            data = data.first()
            return render(request = request,template_name = "userrace_list.html",context={'data':data, 'userRole':userRole})
        
@login_required
def userTrainingListView(request):
    if request.method == 'GET':
        data = UserRace.objects.all().filter(user=request.user)
        userRole = getUserRole(request.user)
        if not data:
            return redirect('training:userRaceAdd')
        else:   
            userData = data.first()
            training = Training.objects.all().filter(race=userData.race)
            weekList = []
            trainFirst = training.first()
            numWeeks = trainFirst.numberOfWeeks-1
            raceDate,weeks = DateUtil.dateWeekStarting(trainFirst.race.end)
            longMiles=0

            for wk in training:
                wk.weeks.totalMiles = wk.weeks.total / userData.avgPace
                if wk.weeks.saturday.type  == 'RUN':
                    longMiles = wk.weeks.saturday.minutes / userData.avgPace
                
                if longMiles==0: 
                    longMiles = wk.weeks.sunday.minutes / userData.avgPace
                
                wk.weeks.longMiles = longMiles
                tmp = wk.race.end - timedelta(days=numWeeks*7)
                wk.weeks.startDate= tmp - timedelta(days=tmp.weekday())
                numWeeks -=1
                weekList.append(wk.weeks)
                longMies =0

            return render(request = request,template_name = "usertraining_list.html",context={'userData':userData, 'week_list':weekList})
