from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from CampusFlow.validators import PHONE_NUMBER_VALIDATOR, USN_VALIDATOR
from CampusFlow.constants import STATE_CHOICES
from CampusFlow.models import Profile
# Create your views here.


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        usn = request.POST['usn']
        name = request.POST['name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number = request.POST['phone_number']
        location = request.POST.get('location')
        print(usn, name , password1, password2, phone_number, location)

        if not usn:
            messages.error(request, 'USN is required!')
            return redirect('register')

        if not name:
            messages.error(request, 'name is required! as per your grade card')
            return redirect('register')


        if password1 != password2:
            messages.error(request, 'Passwords Doesnot Match')
            return redirect('register')

        try: 
            USN_VALIDATOR(usn)
            PHONE_NUMBER_VALIDATOR(phone_number)
        except Exception as e:
            messages.error(request, f"{e}")
            return redirect('register')


        
        try:
            user = User.objects.create_user(username=usn)
            user.set_password(password1)
            user.save()
            profile = Profile.objects.create(user = user, usn=usn,name = name, phone_number=phone_number,location=location)
            profile.save()
            messages.success(request, "Contratulations Your CampusFlow Account has been created")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"{e}")
            return redirect('register')

    context = {
        'state_choices': STATE_CHOICES
    }
    return render(request, "authentication/register.html", context)




def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        usn = request.POST.get('usn')
        password = request.POST.get('password')
        if not usn:
            messages.error(request, "USN is required to Login")
            return redirect("login")
        if not password:
            messages.error(request, "Password is required to Login")
            return redirect("login")
        user = authenticate(username = usn, password = password)
        if user is None:
            messages.error(request, "Wrong Credentials")
            return redirect("login")
        login(request,user)
        return redirect('home')
    return render(request, "authentication/login.html")




@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


    
@login_required
def edit_profile_view(request):
    current_profile = Profile.objects.get(user = request.user)
    if request.method== 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        phone_number = request.POST.get('phone')
        image = request.FILES.get('image')
        location = request.POST.get('location')

        if not name:
            messages.error(request, "name is required")
            return redirect("edit_profile")
        if not phone_number:
            messages.error(request, "phone is required")
            return redirect("edit_profile")
        if not location:
            messages.error(request, "location is required")
            return redirect("edit_profile")
        



        current_profile.name = name
        current_profile.phone_number = phone_number
        current_profile.location = location
        if bio:
            current_profile.bio = bio
        if image:
            current_profile.profile_picture = image

        current_profile.save()
        messages.success(request, "updated successfully")
        return redirect("edit_profile")
    
    context = {
        'state_choices': STATE_CHOICES
    }@login_required
def edit_profile_view(request):
    current_profile = Profile.objects.get(user = request.user)
    if request.method== 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        phone_number = request.POST.get('phone')
        image = request.FILES.get('image')
        location = request.POST.get('location')

        if not name:
            messages.error(request, "name is required")
            return redirect("edit_profile")
        if not phone_number:
            messages.error(request, "phone is required")
            return redirect("edit_profile")
        if not location:
            messages.error(request, "location is required")
            return redirect("edit_profile")
        



        current_profile.name = name
        current_profile.phone_number = phone_number
        current_profile.location = location
        if bio:
            current_profile.bio = bio
        if image:
            current_profile.profile_picture = image

        current_profile.save()
        messages.success(request, "updated successfully")
        return redirect("edit_profile")
    
    context = {
        'state_choices': STATE_CHOICES
    }
    return render(request, "authentication/edit_profile.html", context)
    return render(request, "authentication/edit_profile.html", context)







@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update session to prevent logout after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'authentication/change_password.html', context)



@login_required
def home_view(request):
    return HttpResponse(f"<h1>Hello User {request.user.profile.name}</h1>")