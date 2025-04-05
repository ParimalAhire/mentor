from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import MentorRegisterForm, MenteeRegisterForm
from .models import Profile, Session

# Static pages
def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def mentor_list(request):
    return render(request, "mentor_list.html")

def approach(request):
    return render(request, "approach.html")

def contact(request):
    return render(request, "contact.html")

# Register View

def register_view(request):
    if request.method == 'POST':
        if 'mentor-form' in request.POST:
            form = MentorRegisterForm(request.POST, request.FILES)
            if form.is_valid():
                mentor = form.save()
                auth_login(request, mentor)
                messages.success(request, 'Mentor registration successful! You are now logged in.')
                return redirect('home')
            else:
                messages.error(request, 'Please correct the errors below.')
        elif 'mentee-form' in request.POST:
            form = MenteeRegisterForm(request.POST, request.FILES)
            if form.is_valid():
                mentee = form.save()
                auth_login(request, mentee)
                messages.success(request, 'Mentee registration successful! You are now logged in.')
                return redirect('home')
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        mentor_form = MentorRegisterForm()
        mentee_form = MenteeRegisterForm()

    return render(request, 'register.html', {
        'mentor_form': mentor_form,
        'mentee_form': mentee_form,
    })

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    auth_logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home')

# Profile
@login_required
def mentor_profile(request):
    profile = Profile.objects.get(user=request.user)
    if profile.user_type != 'mentor':
        return redirect('profile')  # fallback if wrong user
    return render(request, 'mentor_profile.html', {'profile': profile})

@login_required
def mentee_profile(request):
    profile = Profile.objects.get(user=request.user)
    if profile.user_type != 'mentee':
        return redirect('profile')  # fallback if wrong user
    return render(request, 'mentee_profile.html', {'profile': profile})

# Mentor List View
@login_required
def mentor_list(request):
    mentors = Profile.objects.filter(user_type='mentor')
    return render(request, 'mentor_list.html', {'mentors': mentors})

# Discover Page
def discover(request):
    mentors = Profile.objects.filter(user_type='mentor')
    sessions = Session.objects.all()
    return render(request, 'discover.html', {
        'mentors': mentors,
        'sessions': sessions
    })

# Booking/scheduling mentorship sessions
@login_required
def available_sessions(request):
    sessions = Session.objects.all()
    sessions = [s for s in sessions if s.remaining_slots() > 0 or request.user.profile in s.mentees.all()]
    return render(request, 'available_sessions.html', {'sessions': sessions})

def session_list(request):
    sessions = Session.objects.all()
    return render(request, 'sessions/session_list.html', {'sessions': sessions})

@login_required
def join_session(request, pk):
    session = get_object_or_404(Session, pk=pk)
    profile = request.user.profile

    # Prevent mentors from joining
    if profile.user_type != 'mentee':
        messages.error(request, "Only mentees can join sessions.")
        return redirect('mentor_list')

    if session.remaining_slots() <= 0:
        messages.error(request, "This session is full.")
        return redirect('available_sessions')

    if profile in session.mentees.all():
        messages.info(request, "You already joined this session.")
    else:
        session.mentees.add(profile)
        messages.success(request, "You successfully joined the session.")

    return redirect('available_sessions')
