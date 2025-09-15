from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)  # Added
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)  # Added
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)  # Added
    portfolio = models.URLField(blank=True, null=True)  # Added
    objective = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)  # Stores JSON array
    experience = models.TextField(blank=True, null=True)  # Stores JSON array
    skills = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)  # Stores JSON array
    languages = models.TextField(blank=True, null=True)  # Added
    certifications = models.TextField(blank=True, null=True)
    awards = models.TextField(blank=True, null=True)  # Added
    organizations = models.TextField(blank=True, null=True)  # Added
    coCurricular = models.TextField(blank=True, null=True)  # Added
    declarations = models.TextField(blank=True, null=True)  # Added
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume for {self.user.username}"