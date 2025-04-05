from django.urls import path
from .views import (
    home, about, mentor_list, approach, contact,
    login_view, logout_view, join_session, available_sessions, 
    discover, mentee_profile, mentor_profile, register_view,
)

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("approach/", approach, name="approach"),
    path("contact/", contact, name="contact"),

    # Authentication URLs
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),

    # Profile URL
    path("mentor/profile/", mentor_profile, name="mentor_profile"),
    path("mentee/profile/", mentee_profile, name="mentee_profile"),

    # Mentor Directory
    path("mentor_list/", mentor_list, name="mentor_list"),

    # Sessions
    path("join_session/<int:pk>/", join_session, name="join_session"),
    path("sessions/available/", available_sessions, name="available_sessions"),

    # Discover page
    path("discover/", discover, name="discover"),
]
