from django.contrib import admin
from .models import Profile, Post, Comment


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "usn", "location", "join_date"]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post)
admin.site.register(Comment)
