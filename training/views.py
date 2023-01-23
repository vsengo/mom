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
from .models import Run, Xtrain, RunWeek, Race, RunSchedule
from .forms import RunForm, XtrainForm, RunWeekForm, RaceForm
from util.date import DateUtil

def getUserRole(user):
    return 'EDIT'

@login_required
def runAddView(request):
    return runUpdView(request,'x')

@login_required
def runUpdView(request,pk):
    if request.method == 'GET':
        if pk=='x':
            form = RunForm()
            run = Run()
        else:
            run = Run.objects.get(id=pk) 

        form  = RunForm(instance = run)
        form_name="Run"
        return render(request,template_name='common_form.html',context={'form':form, 'form_name':form_name})

    if request.method == 'POST':
        form = RunForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            if pk != 'x':
                obj.id=pk
            obj.save()
            print("Saved "+str(pk))
        else:
            error={'message':'Error in Data input to Run'}
            return render(request,template_name='error.html',context=error)

        return redirect('training:runList')



@login_required
def runListView(request):
    if request.method == 'GET':
        runs = Run.objects.all()
        userRole = getUserRole(request.user)
        return render(request = request,template_name = "run_list.html",context={'run_list':runs, 'userRole':userRole})

 
@login_required
def runDelView(request,pk):
    run = Run.objects.get(id=pk)
    run.delete()        
    return redirect('training:runList')

@login_required
def xtrainAddView(request):
    return xtrainUpdView(request,'x')

@login_required
def xtrainUpdView(request,pk):
    if request.method == 'GET':
        if pk=='x':
            form = XtrainForm()
            run = Xtrain()
        else:
            run = Xtrain.objects.get(id=pk) 

        form  = XtrainForm(instance = run)
        form_name="XTrain"
        return render(request,template_name='common_form.html',context={'form':form, 'form_name':form_name})

    if request.method == 'POST':
        form = XtrainForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            if pk != 'x':
                obj.id=pk
            obj.save()
            print("Saved "+str(pk))
        else:
            error={'message':'Error in Data input to Run'}
            return render(request,template_name='error.html',context=error)

        return redirect('training:xtrainList')

@login_required
def xtrainListView(request):
    if request.method == 'GET':
        data = Xtrain.objects.all()
        userRole = getUserRole(request.user)
        return render(request = request,template_name = "xtrain_list.html",context={'data_list':data, 'userRole':userRole})

@login_required
def xtrainDelView(request,pk):
    data = Xtrain.objects.get(id=pk)
    data.delete()        
    return redirect('training:xtrainList')

@login_required
def runWeekAddView(request):
    return runWeekUpdView(request,'x')

@login_required
def runWeekUpdView(request,pk):
    if request.method == 'GET':
        if pk=='x':
            form = RunWeekForm()
            run = RunWeek()
        else:
            run = RunWeek.objects.get(id=pk) 

        form  = RunWeekForm(instance = run)
        form_name="RunWeek"
        return render(request,template_name='common_form.html',context={'form':form, 'form_name':form_name})

    if request.method == 'POST':
        form = RunWeekForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            if pk != 'x':
                obj.id=pk
            obj.save()

            obj.total = obj.run_1.distance + obj.run_2.distance + obj.run_3.distance+obj.run_4.distance
            obj.save(update_fields=['total'])
        
            print("Saved "+str(pk))
        else:
            error={'message':'Error in Data input to Run'}
            return render(request,template_name='error.html',context=error)

        return redirect('training:runWeekList')

@login_required
def runWeekListView(request):
    if request.method == 'GET':
        data = RunWeek.objects.all()
        userRole = getUserRole(request.user)
        return render(request = request,template_name = "runweek_list.html",context={'data_list':data, 'userRole':userRole})

@login_required
def runWeekDelView(request,pk):
    data = RunWeek.objects.get(id=pk)
    data.delete()        
    return redirect('training:runWeekList')

def runScheduleView(request,pk):
    if request.method == 'GET':
        wk=DateUtil.dateWeekStarting()

        data = RunSchedule.objects.filter(race_id=pk)
        race = Race.objects.get(id=pk)
        userRole = 'VIEW'
        context={
            'data_list':data,
            'race':race,
            'week_start':wk,
            'userRole':userRole,
        }
        return render(request = request,template_name = "runschedule.html",context=context)

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
            print("Saved "+str(pk))
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