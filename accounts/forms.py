from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from util.widgets import BootstrapDateTimePickerInput
from .models import Member 

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "First Name")
    last_name = forms.CharField(label = "Last Name")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label = "First Name")
    last_name = forms.CharField(label = "Last Name")

    class Meta:
        model=User
        fields = ("first_name","last_name","email")

class MemberForm(forms.ModelForm):
    mobile =forms.CharField(label="Mobile Number (countrycode number)")
    city = forms.CharField(label = "City")
    country = forms.CharField(label = "Country")
    dob = forms.DateField(label = "Date of Birth(YYYY-MM-DD)",)
    widgets = {
            'dob': BootstrapDateTimePickerInput(format='%Y-%m-%d'), # specify date-frmat
        }
    class Meta:
        model = Member
        fields = ("mobile","city", "country", "dob",'photo')
    
    def save(self,commit=True):
        member = super(MemberForm,self).save(commit=False)
        if commit:
            member.save()
        return member

class MemberChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%s %s" % (obj.first_name, obj.last_name)
