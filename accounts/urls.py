from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,re_path,include
from .views import  SignUpView, deleteMember, logOff, logIn, memberView, change_password, pwdResetInstruction

urlpatterns = [
    re_path(r'signup', SignUpView.as_view(), name='signup'),
    re_path(r'logoff', logOff, name='logoff'),
    re_path(r'login', logIn, name='login'),
    re_path(r'^member$', memberView, name='member'),
    re_path(r'^change_password/$', change_password, name='change_password'),
    re_path(r'pwdResetInstruction$', pwdResetInstruction, name='pwdResetInstruction'),

    re_path(r'password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset/pwdreset_form.html',
             subject_template_name='accounts/password_reset/pwdreset_subject.txt',
             email_template_name='accounts/password_reset/pwdreset_email.html',
             success_url='login'
         ),
         name='password_reset'),
    
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset/pwdreset_confirm.html',
             success_url='login'),
         name='password_reset_confirm'),

    re_path(r'password_reset_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset/pwdreset_complete.html'),
         name='password_reset_complete'),
]