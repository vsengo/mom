from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from util.widgets import BootstrapDateTimePickerInput
from .models import Activity, Race, WeeklyActivity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('name','type','detail','distance','minutes')
    
    def save(self,commit=True):
        data = super(ActivityForm,self).save(commit=False)
        if commit:
            data.save()
        return data
    
class WeeklyActivityForm(forms.ModelForm):
    class Meta:
        model = WeeklyActivity
        fields = "__all__"
    
    def save(self,commit=True):
        data = super(WeeklyActivityForm,self).save(commit=False)
        if commit:
            data.save()
        return data

class RaceForm(forms.ModelForm):
    widgets = {
        'start': BootstrapDateTimePickerInput(format='%Y-%m-%d'), # specify date-frmat
        'end'  : BootstrapDateTimePickerInput(format='%Y-%m-%d'), # specify date-frmat
    }
    class Meta:
        model = Race
        fields = "__all__"
    
    def save(self,commit=True):
        data = super(RaceForm,self).save(commit=False)
        if commit:
            data.save()
        return data