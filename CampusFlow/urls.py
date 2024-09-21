from django.urls import path
from CampusFlow.views import (register_view,login_view, home_view, logout_view)



urlpatterns = [
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/',logout_view , name='logout'),
    path('home/',home_view , name='home'),
]
