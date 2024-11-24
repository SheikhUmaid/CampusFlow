from django.db import models
from django.contrib.auth.models import User
from CampusFlow.validators import (USN_VALIDATOR,PHONE_NUMBER_VALIDATOR)
from CampusFlow.constants import STATE_CHOICES, CAMPUS_LOCATIONS,ADVERTISEMENT_LOCATIONS,RAPPORT_REQUEST_STATUSES
import os
from PIL import Image
# Create your models here.

def get_profile_image_upload_path(instance, filename):
    # This will save the file in the directory "profile_images/<usn>/<filename>"
    return os.path.join(f"profile_images/{instance.usn}/", filename)

def get_post_image_upload_path(instance, filename):
    # This will save the post images in the directory "post_images/<usn>/<filename>"
    return os.path.join(f"post_images/{instance.user.user.username}/", filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usn = models.CharField(max_length=12,unique=True, validators=[USN_VALIDATOR])
    name = models.CharField(max_length=35)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=get_profile_image_upload_path, default= "profile_images/default/default_image.png")
    phone_number = models.CharField(max_length=10,unique=True, validators=[PHONE_NUMBER_VALIDATOR])
    email = models.EmailField(max_length=254, blank=True)
    join_date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=2, choices=STATE_CHOICES, default="OC")
    rapport = models.ManyToManyField('self', blank=True, symmetrical=True)
    exclusive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usn} - {self.name}"

class Post(models.Model):
    title = models.CharField(max_length=100, default="", blank=True, )
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to = get_post_image_upload_path)
    caption = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name="liked_posts",blank=True)
    location = models.CharField(max_length=2,choices=CAMPUS_LOCATIONS, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"post by {self.user.name} usn {self.user.usn} pk {self.user.pk}"
    
        
    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_comments",blank=True)

    def __str__(self):
        return f"Comment by {self.user.usn} on {self.post.user.usn}'s post"
    
class Advertisement(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(upload_to="ads",)
    event_date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=2,choices=ADVERTISEMENT_LOCATIONS,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.event_date}"
    
class RapportRequest(models.Model):
    by_user = models.ForeignKey(Profile, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, related_name='received_requests', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255,blank=True)
    status = models.CharField(max_length=10, choices=RAPPORT_REQUEST_STATUSES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Request from {self.by_user} to {self.to_user} ({self.status})"
    
