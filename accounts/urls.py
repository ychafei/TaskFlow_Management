from django.urls import path
from .views import signup_view, login_view, profile_view, CustomLogoutView
from .views import edit_profile_view 

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", profile_view, name="profile"),
     path("edit-profile/", edit_profile_view, name="edit_profile"),
]

