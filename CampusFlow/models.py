from django.db import models
from django.contrib.auth.models import User
from CampusFlow.validators import (USN_VALIDATOR,PHONE_NUMBER_VALIDATOR)
from CampusFlow.constants import STATE_CHOICES
# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usn = models.CharField(max_length=12,unique=True, validators=[USN_VALIDATOR])
    name = models.CharField(max_length=35)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profile_images/", blank=True)
    phone_number = models.CharField(max_length=10,unique=True, validators=[PHONE_NUMBER_VALIDATOR])
    join_date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True)


    def __str__(self):
        return f"{self.usn} - {self.name}"
    
    

