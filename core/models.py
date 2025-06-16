from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"