from django.db import models
from datetime import timedelta, datetime,date
from django.contrib.auth.models import User


class Activity(models.Model):
    Activity_type = [
        ('RUN','Run'),
        ('XTRAIN', 'XTrain'),
        ('REST','Rest')
    ]
    type = models.CharField(max_length=16,choices=Activity_type)
    name = models.CharField(max_length=64)
    distance = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
    detail = models.CharField(max_length=512,null=True,blank=True)
    minutes = models.SmallIntegerField(null=True,blank=True)
    url  = models.URLField(null=True,blank=True)

    def __str__(self):
        return "%s"%(self.name)
    
    def avgPaceInMin(self):
        avgPace=self.distance/self.minutes
        m=int(avgPace)
        s = 60*(avgPace - m)
        dt= date.today()
        return datetime(dt.year,dt.month,dt.day,minute=m,second=s)
    
class WeeklyActivity(models.Model):
    week = models.SmallIntegerField()
    name = models.CharField(max_length=64,default="")
    monday = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="monday")
    tuesday = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="tuesday")
    wednesday = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="wednesday")
    thursday = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="thursday") 
    friday = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="friday") 
    saturday = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="saturday") 
    sunday = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="sunday") 
    
    total = models.SmallIntegerField(default=0)
    totalMiles = models.FloatField(default=0)
    longMiles = models.FloatField(default=0)
    startDate = models.DateField(null=True)
  
class Race(models.Model):
    name = models.CharField(max_length=128)
    distance = models.DecimalField(max_digits=4,decimal_places=2)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return "%s"%(self.name)
    

class Training(models.Model):
    race = models.ForeignKey(Race,on_delete=models.CASCADE,related_name="race")
    weeks=models.ForeignKey(WeeklyActivity, on_delete=models.CASCADE,related_name="weeks")
    numberOfWeeks = models.SmallIntegerField()
    
class UserRace(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
    race = models.ForeignKey(Race,on_delete=models.CASCADE,related_name="user_race")
    targetTimeInMin = models.SmallIntegerField()
    avgPace = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    easyPace = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    tempoPace = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    vo2Pace = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    speedPace = models.DecimalField(default=0, max_digits=4, decimal_places=2)

    def paceInMin(self, pace):
        m=int(pace)
        s = 60*(pace - m)
        dt= date.today()
        return datetime(dt.year,dt.month,dt.day,minute=m,second=s)
    def avgPaceInMin(self):
        return self.paceInMin(self.avgPace)
    def easyPaceInMin(self):
        return self.paceInMin(self.easyPace)
    def tempoPaceInMin(self):
        return self.paceInMin(self.tempoPace)
    def vo2PaceInMin(self):
        return self.paceInMin(self.vo2Pace)
    def speedPaceInMin(self):
        return self.paceInMin(self.speedPace)
    