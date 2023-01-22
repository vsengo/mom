from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from util.widgets import BootstrapDateTimePickerInput
from .models import Run, Xtrain, RunWeek, Race


class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ('name','detail','distance','avgPace')
    
    def save(self,commit=True):
        data = super(RunForm,self).save(commit=False)
        if commit:
            data.save()
        return data

class XtrainForm(forms.ModelForm):
    class Meta:
        model = Xtrain
        fields = ('name','detail','minutes','url')
    
    def save(self,commit=True):
        data = super(XtrainForm,self).save(commit=False)
        if commit:
            data.save()
        return data

class RunWeekForm(forms.ModelForm):
    class Meta:
        model = RunWeek
        fields = "__all__"
    
    def save(self,commit=True):
        data = super(RunWeekForm,self).save(commit=False)
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