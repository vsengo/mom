from django.db import models
from datetime import timedelta, datetime,date

# Create your models here.
class Run(models.Model):
    distance = models.DecimalField(max_digits=4,decimal_places=2)
    avgPace = models.DecimalField(max_digits=4, decimal_places=2)
    detail = models.CharField(max_length=256)
    name = models.CharField(max_length=64)

    def __str__(self):
        return "%s"%(self.name)
    
    def avgPaceInMin(self):
        m=int(self.avgPace)
        s = 60*(self.avgPace - m)
        dt= date.today()
        return datetime(dt.year,dt.month,dt.day,minute=m,second=s)
    
    
    
class Xtrain(models.Model):
    name = models.CharField(max_length=64)
    minutes = models.SmallIntegerField()
    detail = models.CharField(max_length=256)
    url  = models.URLField()

    def __str__(self):
        return self.name

class RunWeek(models.Model):
    WEEKDAYS = [
        ('MONDAY','Monday'),
        ('TUESDAY','Tuesday'),
        ('WEDNESDAY','Wednesday'),
        ('THURSDAY','Thursday'),
        ('FRIDAY','Friday'),
        ('SATURDAY','Saturday'),
        ('SUNDAY','Sunday'),
    ]
    week = models.SmallIntegerField()
    name = models.CharField(max_length=64,default="")
    day_1 = models.CharField(max_length=10, choices=WEEKDAYS)
    run_1 = models.ForeignKey(Run, on_delete=models.CASCADE, related_name="run_1")
    day_2 = models.CharField(max_length=10, choices=WEEKDAYS)
    run_2 = models.ForeignKey(Run, on_delete=models.CASCADE, related_name="run_2")
    day_3 = models.CharField(max_length=10, choices=WEEKDAYS)
    run_3 = models.ForeignKey(Run, on_delete=models.CASCADE, related_name="run_3")
    day_4 = models.CharField(max_length=10, choices=WEEKDAYS)
    run_4 = models.ForeignKey(Run, on_delete=models.CASCADE, related_name="run_4") 
    restday_1 = models.CharField(max_length=10, choices=WEEKDAYS)
    xtrain_1  = models.ForeignKey(Xtrain, on_delete=models.CASCADE, related_name="xtrain_1")
    restday_2 = models.CharField(max_length=10, choices=WEEKDAYS)
    xtrain_2  = models.ForeignKey(Xtrain,on_delete=models.CASCADE, related_name="xtrain_2")
    restday_3 = models.CharField(max_length=10, choices=WEEKDAYS)
    xtrain_3  = models.ForeignKey(Xtrain,on_delete=models.CASCADE, related_name="xtrain_3")
    
    total = models.SmallIntegerField(default=0)


class Race(models.Model):
    numberOfWeeks = models.SmallIntegerField()
    name = models.CharField(max_length=128)
    distance = models.DecimalField(max_digits=4,decimal_places=2)
    start = models.DateField()
    end = models.DateField()

class RunSchedule(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    runWeek = models.ForeignKey(RunWeek, on_delete=models.CASCADE, related_name="runweek") 

    def week(self):
        return self.race.start + timedelta(days=7*(self.runWeek.week-2))
    def total(self):
        return self.runWeek.total
    def day_1(self):
        return self.runWeek.day_1
    def run_1(self):
        return self.runWeek.run_1
    def day_2(self):
        return self.runWeek.day_2
    def run_2(self):
        return self.runWeek.run_2
    def day_3(self):
        return self.runWeek.day_3
    def run_3(self):
        return self.runWeek.run_3
    def day_4(self):
        return self.runWeek.day_4
    def run_4(self):
        return self.runWeek.run_4
    def restday_1(self):
        return self.runWeek.restday_1
    def xtrain_1(self):
        return self.runWeek.xtrain_1
    def restday_2(self):
        return self.runWeek.restday_2
    def xtrain_2(self):
        return self.runWeek.xtrain_2
    def restday_3(self):
        return self.runWeek.restday_3
    def xtrain_3(self):
        return self.runWeek.xtrain_3
 