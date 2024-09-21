from django.contrib import admin
from .models import Profile
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'usn', 'location', 'join_date']

admin.site.register(Profile, ProfileAdmin)