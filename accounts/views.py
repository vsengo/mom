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
from rest_framework.response import Response
from rest_framework.decorators import api_view
from  django_pandas.io import read_frame

from django.db.models import Sum, Count
from django.conf import settings
from django.http import JsonResponse
from os import path, rename
from util import img
from PIL import Image
from datetime import datetime
from django.utils  import timezone
from .models import Member
from accounts.forms import RegisterForm, UserForm, MemberForm

class SignUpView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'signup.html'

def logIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                c =  {'user_id':user.id,
                     'name':user.first_name
                     }
                t = loader.get_template('home/base.html')
                #request.user = user
                return  render(request = request,template_name = "home/index.html",context=c)
            else:
                return render(request=request,template_name="error.html", context={'title':"Login ERROR", 'message':"User name <strong>"+username+"</strong> or Password is wrong"})
        else:
            return render(request=request,template_name="error.html", context={'title':"Login ERROR", 'message':"User name or Password is wrong"})

    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def pwdResetInstruction(request):
    return render(request, 'password_reset/pwdreset_instruction.html')

@login_required
def deleteMember(request):
    member = Member.objects.get(user_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    logout(request)
    try:
        user.delete()
    except IntegrityError as e:
        user.is_active=0
        user.username=user.username+"DELETED"
        user.save(update_fields=['is_active'])

    return redirect('/')

@login_required
def memberView(request):
    member = Member.objects.get(user_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        transaction = Transaction.objects.all().filter(owner_id=user.id).order_by('-date')

    return render(request = request,template_name = "member.html",context={'member':member, 'transaction_list':transaction})

@login_required
def memberUpdView(request):
    member = Member.objects.get(user_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'GET':
        profile_form = MemberForm(instance=member)

        user_form = UserForm(instance=user)
        return render(request = request,template_name = "member_upd.html",context={"profile_form":profile_form, 'user_form':user_form, 'member':member})

    if request.method == 'POST':
        member_form = MemberForm(request.POST,request.FILES, instance=request.user.member)
        user_form = UserForm(request.POST,instance=request.user)
        if user_form.is_valid():
            obj=user_form.save(commit=False)
            obj.save(update_fields=['first_name','last_name','email'])

        if member_form.is_valid():
            obj=member_form.save(commit=False)
            user = User.objects.get(id=request.user.id)
            obj.user = user
            obj.id=member.id
            obj.save()
            
            if obj.photo:
                today = datetime.now()
                twidth, theight = 150, 200
                fname, ext = path.splitext(obj.photo.name)
                albumPath = path.join(settings.MEDIA_ROOT, "profile/")
                opath = path.join(settings.MEDIA_ROOT,fname + ext)
                nfname = today.strftime("%m%dT%H%M%S") + ext
                npath = path.join(albumPath,nfname)
                photo = Image.open(opath)
                width, height = photo.size
                if (width > twidth):
                    photo = img.apply_orientation(photo)
                    photo.thumbnail((twidth, theight), Image.HAMMING)
                photo.save(opath)
                rename(opath,npath)
                obj.photo.name = "profile/"+nfname
                obj.save()
                messages.success(request, "Profile information was updated. Successfully")

        return redirect('accounts:member')

@login_required
def logOff(request):
    logout(request)
    user = User.objects.filter(username=request.user)
    return render(request, 'logoff.html',{'user':user})







