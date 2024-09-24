from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from CampusFlow.validators import PHONE_NUMBER_VALIDATOR, USN_VALIDATOR
from CampusFlow.constants import STATE_CHOICES, CAMPUS_LOCATIONS
from CampusFlow.models import Profile, Post, Comment

# Create your views here.



def landing_view(request):
    return render(request, "base/landing_page.html")



def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        usn = request.POST["usn"]
        name = request.POST["name"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        phone_number = request.POST["phone_number"]
        location = request.POST.get("location")
        print(usn, name, password1, password2, phone_number, location)

        if not usn:
            messages.error(request, "USN is required!")
            return redirect("register")

        if not name:
            messages.error(request, "name is required! as per your grade card")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords Doesnot Match")
            return redirect("register")

        try:
            USN_VALIDATOR(usn)
            PHONE_NUMBER_VALIDATOR(phone_number)
        except Exception as e:
            messages.error(request, f"{e}")
            return redirect("register")

        try:
            user = User.objects.create_user(username=usn)
            user.set_password(password1)
            user.save()
            profile = Profile.objects.create(
                user=user,
                usn=usn,
                name=name,
                phone_number=phone_number,
                location=location,
            )
            profile.save()
            messages.success(
                request, "Contratulations Your CampusFlow Account has been created"
            )
            return redirect("login")
        except Exception as e:
            messages.error(request, f"{e}")
            return redirect("register")

    context = {"state_choices": STATE_CHOICES}
    return render(request, "authentication/register.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        usn = request.POST.get("usn")
        password = request.POST.get("password")
        if not usn:
            messages.error(request, "USN is required to Login")
            return redirect("login")
        if not password:
            messages.error(request, "Password is required to Login")
            return redirect("login")
        user = authenticate(username=usn, password=password)
        if user is None:
            messages.error(request, "Wrong Credentials")
            return redirect("login")
        login(request, user)
        return redirect("home")
    return render(request, "authentication/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def edit_profile_view(request):
    current_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        name = request.POST.get("name")
        bio = request.POST.get("bio")
        phone_number = request.POST.get("phone")
        image = request.FILES.get("image")
        location = request.POST.get("location")

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

    context = {"state_choices": STATE_CHOICES}
    return render(request, "authentication/edit_profile.html", context)


@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update session to prevent logout after password change
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("change_password")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    context = {
        "form": form,
    }
    return render(request, "authentication/change_password.html", context)


@login_required
def home_view(request):
    posts = Post.objects.all()
    context={"posts":posts}
    return render(request, "base/home_page.html", context)


@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    context = {"post": post, "comments": comments}
    return render(request, "media/post_detail.html", context)

@login_required
def add_comment(request, post_id):
    user = request.user
    profile = user.profile
    post = get_object_or_404(Post, pk=post_id)
    print(profile.name)
    if request.method == "POST":
        content = request.POST.get("content")
        if not content:
            messages.error(request, "Comment is required to fill this form")
            return redirect("post_detail", post_id = post_id)
        comment = Comment.objects.create(user = profile, content= content, post=post)
        comment.save()
        messages.success(request, "Comment added successfully")
        
        return redirect("post_detail", post_id=post_id)
    return redirect("post_detail", post_id=post_id)


@login_required
def toggle_like(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    
    if user in post.likes.all():
        print(1)
        post.likes.remove(user)
    else:
        print(2)
        post.likes.add(user)
        
    post.save()
    return redirect("post_detail", post_id= post_id)




@login_required
def upload_post_view(request):
    user = request.user
    profile = user.profile
    if request.method == "POST":
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        location = request.POST.get('location')        
        if not image:
            messages.error(request, "Image is required to upload a post.")
            return redirect("upload_post")
        if not location:
            messages.error(request, "Please select a location.")
            return redirect("upload_post")
        post = Post.objects.create(user = profile, image = image, location=location)
        if caption:
            post.caption = caption
        post.save()
        
        messages.success(request, "Post uploaded successfully.")
        return redirect("post_detail", post.pk)
    context = {"locations": CAMPUS_LOCATIONS}
    return render(request, "media/post_upload.html", context)


@login_required
def delete_post(request, post_id):
    user = request.user
    profile = user.profile
    post = get_object_or_404(Post, pk = post_id)
    if post.user != profile:
        messages.error(request, "You're Not authorized to perform this action")
        return redirect("home")
    post.delete()
    
    messages.success(request, "Post deleted successfully.")

    # Redirect to the home or profile page
    return redirect("home")
    
    

@login_required
def edit_post_view(request, post_id):
    user = request.user
    profile = user.profile
    post = get_object_or_404(Post, pk=post_id)
    
    # Ensure only the owner can edit the post
    if post.user != profile:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect("home")
    
    if request.method == "POST":
        caption = request.POST.get("caption")
        location = request.POST.get("location")
        
        # Handle empty caption or location
        if caption:
            post.caption = caption
        else:
            messages.warning(request, "Caption was left unchanged.")
        
        if location:
            post.location = location
        else:
            messages.warning(request, "Location was left unchanged.")
        
        post.save()
        messages.success(request, "Post has been updated successfully.")
        return redirect("post_detail", post_id=post.id)  # Redirect after updating
    
    context = {"post": post, "locations": CAMPUS_LOCATIONS}
    return render(request, "media/post_edit_view.html", context)
