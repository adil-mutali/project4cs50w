
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/new", views.new_post, name='new'),
    path("<int:user_id>", views.profile, name='profile'),
    path("follow_unfollow/<int:id>", views.follow_unfollow, name="follow"),
    path("following", views.following, name="following"),
    path("editposts", views.edit_posts, name='edit')
]
