from django.contrib import admin
from .models import Profile, Post, Comment,Advertisement


# Register your models here.



admin.site.site_header = "CampusFlow Administration Panel"
admin.site.site_title = "CampuaFlow Admin Panel"
admin.site.index_title = "Welcome to the CampusFlow Admin Panel"
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "usn", "location", "join_date"]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Advertisement)