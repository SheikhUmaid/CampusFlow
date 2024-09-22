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
    toggle_like
)


urlpatterns = [
    path("auth/register/", register_view, name="register"),
    path("auth/login/", login_view, name="login"),
    path("auth/logout/", logout_view, name="logout"),
    path("auth/edit-profile", edit_profile_view, name="edit_profile"),
    path("auth/change-password", change_password_view, name="change_password"),
    path("post/<int:post_id>", post_detail_view, name="post_detail"),
    path("post/post-comment/<int:post_id>", add_comment, name="add_comment"),
    path("post/post-like/<int:post_id>", toggle_like, name="toggle_like"),
    path("home/", home_view, name="home"),
]
