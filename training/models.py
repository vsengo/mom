from django.db import models
from datetime import timedelta, datetime,date

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

class Race(models.Model):
    name = models.CharField(max_length=128)
    distance = models.DecimalField(max_digits=4,decimal_places=2)
    start = models.DateField()
    end = models.DateField()

class Training(models.Model):
    race = models.ForeignKey(Race,on_delete=models.CASCADE,related_name="race")
    weeks=models.ForeignKey(WeeklyActivity, on_delete=models.CASCADE,related_name="weeks")
    numberOfWeeks = models.SmallIntegerField()
    