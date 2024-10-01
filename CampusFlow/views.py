from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from CampusFlow.validators import PHONE_NUMBER_VALIDATOR, USN_VALIDATOR
from CampusFlow.constants import STATE_CHOICES, CAMPUS_LOCATIONS
from CampusFlow.models import Profile, Post, Comment, RapportRequest
from CampusFlow.integrations import safe_search_detection


def landing_view(request):
    if request.user.is_authenticated:
        return redirect("home")
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
    return redirect("landing")

@login_required
def edit_profile_view(request):
    current_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        name = request.POST.get("name")
        bio = request.POST.get("bio")
        phone_number = request.POST.get("phone")
        image = request.FILES.get("image")
        email = request.POST.get("email")
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
        if email:
            current_profile.email = email

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
    rapports = request.user.profile.rapport.all()
    print(rapports)
    posts = Post.objects.filter(user__in=rapports)
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
            
            
        # Perform SafeSearch detection on the uploaded image
        safe = safe_search_detection(post.image.path)
        
        print(safe.adult)
        if safe.adult>=3:
            messages.error(request, "The uploaded image contains adult content.")
            post.delete()
            return redirect("upload_post")
        
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

@login_required
def profile_page_view(request, user_id):
    target_user = get_object_or_404(Profile, pk=user_id)
    # Check if a pending request exists
    existing_request = RapportRequest.objects.filter(
        by_user=request.user.profile, to_user=target_user, status='pending'
    ).exists()

    # Check if the current user and the target user are already friends
    is_friend = request.user.profile in target_user.rapport.all()

    # Set flags for the template context
    request_exists = 1 if existing_request else 0
    friend_status = 1 if is_friend else 0

    context = {
        "user": target_user,
        "existing_request": request_exists,
        "is_friend": friend_status,
    }
    
    return render(request, "user/profile.html", context)

@login_required
def notifications_view(request):
    requests = RapportRequest.objects.filter(to_user= request.user.profile, status="pending")
    context = {"requests":requests}
    return render(request,"user/notifications.html", context)

@login_required
def send_rapport_request(request, user_id):
    profile = request.user.profile
    target_user = get_object_or_404(Profile, pk=user_id)

    # Check if there is already a pending request between these two users
    existing_request = RapportRequest.objects.filter(
        by_user=profile, to_user=target_user, status='pending'
    ).exists()

    if existing_request:
        messages.error(request, "Rapport request already sent.")
        return redirect("profile_view", user_id=target_user.pk)

    # Check if the target user has already sent a request to the current user
    reverse_request = RapportRequest.objects.filter(
        by_user=target_user, to_user=profile, status='pending'
    ).exists()

    if reverse_request:
        messages.error(request, "The target user has already sent you a request.")
        return redirect("profile_view", user_id=target_user.pk)

    # If no requests exist, create a new rapport request
    rapport_request = RapportRequest.objects.create(by_user=profile, to_user=target_user)
    messages.success(request, "Rapport request sent successfully.")
    return redirect("profile_view", user_id=target_user.pk)

@login_required
def accept_rapport_request(request, request_id):
    
    rapport_request = get_object_or_404(RapportRequest, id=request_id)

    if rapport_request.to_user != request.user.profile:
        messages.error(request, "You are not authorized to accept this request.")
        return redirect("notifications")

    # Add rapport relationship (mutual following)
    rapport_request.to_user.rapport.add(rapport_request.by_user)
    rapport_request.by_user.rapport.add(rapport_request.to_user)

    # Delete the rapport request as it is now accepted
    rapport_request.status = "accepted"
    rapport_request.save()

    messages.success(request, f"You are now connected with {rapport_request.by_user.name}!")
    return redirect("notifications")

@login_required
def reject_rapport_request(request, request_id):

    rapport_request = get_object_or_404(RapportRequest, id=request_id)

    if rapport_request.to_user != request.user.profile:
        messages.error(request, "You are not authorized to accept this request.")
        return redirect("notifications")

    # Delete the rapport request as it is now accepted
    rapport_request.delete()

    messages.success(request, f"{rapport_request.by_user.name}'s Request has been rejected successfully")
    return redirect("notifications")

@login_required
def user_search_view(request):
    query = request.GET.get('q')
    results = None
    print(query)
    
    if query:
        results = Profile.objects.filter(
            Q(name__icontains=query) |
            Q(usn__icontains = query)
        )
        
    context = {
        'results': results,
        'query': query,
    }
    
# <<<<<<< HEAD
    return render(request, "user/search.html",context)




def explore_view(request):
    # public_profiles = Profile.objects.filter(exclusive=False)
    # random_posts = Post.objects.filter(user__in=public_profiles)
    

    public_profiles = Profile.objects.filter(exclusive=False)
    random_posts = Post.objects.filter(user__in=public_profiles).order_by('?')
    context = {"posts": random_posts}
    return render(request,"media/explore.html", context)


def create_random_post(request):
    # Generate a random image URL (using picsum.photos)
    image_url = "https://picsum.photos/800/800"
    
    fake = Faker()
    user = choice(Profile.objects.all())  # Select a random user from profiles
    
    # Fetch the image from the URL
    response = requests.get(image_url)
    
    if response.status_code == 200:
        # Open the image using BytesIO and Pillow
        image = Image.open(BytesIO(response.content))
        
        # Save the image temporarily
        image_name = f"temp_{fake.uuid4()}.jpg"  # Use a unique name for each image
        image.save(f"media/{image_name}")  # Save in the media folder or a specific path
        
        # Create the Post object with the saved image
        post = Post.objects.create(user=user, image=f"{image_name}")
        post.save()

        return HttpResponse("Post Created Successfully")
    else:
        return HttpResponse("Failed to fetch the image", status=400)