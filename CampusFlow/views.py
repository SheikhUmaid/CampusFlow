from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from CampusFlow.validators import PHONE_NUMBER_VALIDATOR, USN_VALIDATOR
from CampusFlow.constants import STATE_CHOICES
from CampusFlow.models import Profile
# Create your views here.


def register_view(request):

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
    return render(request, "authentication/login.html")