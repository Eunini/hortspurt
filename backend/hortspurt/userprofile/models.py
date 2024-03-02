from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """User's profile"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('P', 'Prefer not to say'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_balance = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='P')
    # phone_no = models.CharField(max_length=11)