from .models import Member, Transaction, Beneficiary, Project
from django.contrib.auth.models import User


from rest_framework import serializers

class MemberPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Member
        fields = ['mobile']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['first_name','last_name','email']
