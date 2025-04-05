from django.db import models
from django.contrib.auth.models import User

# Extended user profile for mentors and mentees
class Profile(models.Model):
    USER_TYPES = (
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    availability = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"

# Booking/scheduling mentorship sessions
# models.py

class Session(models.Model):
    mentor = models.ForeignKey(Profile, related_name='mentoring_sessions', on_delete=models.CASCADE)
    mentees = models.ManyToManyField(Profile, related_name='group_sessions')
    topic = models.CharField(max_length=255)
    scheduled_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    zoom_link = models.URLField(max_length=500, blank=True)
    is_completed = models.BooleanField(default=False)
    capacity = models.PositiveIntegerField(default=5)  # Optional: limit number of mentees

    def __str__(self):
        return f"{self.topic} ({self.mentor.user.username})"

    def remaining_slots(self):
        return self.capacity - self.mentees.count()

# Feedback after session
class Feedback(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)  # 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.session.mentee.user.username} for {self.session.mentor.user.username}"

# Resource Library
class Resource(models.Model):
    CATEGORY_CHOICES = (
        ('article', 'Article'),
        ('video', 'Video'),
        ('case_study', 'Case Study'),
        ('research', 'Research Paper'),
        ('other', 'Other'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
