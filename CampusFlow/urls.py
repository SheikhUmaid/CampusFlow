from django.urls import path
from CampusFlow.views import (
    register_view,
    login_view,
    home_view,
    logout_view,
    edit_profile_view,
    change_password_view,
    post_detail_view,
    add_comment,
    toggle_like,
    landing_view,
    upload_post_view,
    delete_post,
    edit_post_view,
    profile_page_view,
    notifications_view,
    accept_rapport_request,
    send_rapport_request,
    reject_rapport_request
)


urlpatterns = [
    path("", landing_view, name="landing"),
    
    path("auth/register/", register_view, name="register"),
    path("auth/login/", login_view, name="login"),
    path("auth/logout/", logout_view, name="logout"),
    path("auth/edit-profile/", edit_profile_view, name="edit_profile"),
    path("auth/change-password/", change_password_view, name="change_password"),
    
    path("post/<int:post_id>/", post_detail_view, name="post_detail"),
    path("post/post-comment/<int:post_id>/", add_comment, name="add_comment"),
    path("post/post-like/<int:post_id>/", toggle_like, name="toggle_like"),
    path("post/upload/", upload_post_view, name="upload_post"),
    path("post/delete/<int:post_id>/", delete_post, name="delete_post"),
    path("post/edit/<int:post_id>/", edit_post_view, name="edit_post"),
    
    path("user/<int:user_id>", profile_page_view, name="profile_view"),
    path("user/notifications", notifications_view, name="notifications"),
    path("user/rapport/accept/<int:request_id>", accept_rapport_request, name="accept_rapport"),
    path('user/rapport/send/<int:user_id>',send_rapport_request, name="send_rapport_request"),
    path('user/rapport/reject/<int:request_id>',reject_rapport_request, name="reject_rapport"),
    
    path("home/", home_view, name="home"),
]
