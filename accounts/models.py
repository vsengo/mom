from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils  import timezone

class UserRole:
    EDIT='EDIT'
    VIEW='VIEW'
    NONE='NONE'
    
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.TextField(max_length=12, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)    
    photo = models.ImageField(upload_to='profile/',blank=True, null=True)

    def __str__(self):
        return "%s %" % (self.first_name,self.last_name) 

@receiver(post_save, sender=User)
def create_user_member(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_member(sender, instance, **kwargs):
    instance.member.save()

