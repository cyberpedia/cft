# api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class Team(models.Model):
    """
    Represents a team in the CTF platform.
    """
    name = models.CharField(max_length=100, unique=True, help_text="The name of the team.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Includes CTF-specific fields like score and team affiliation.
    """
    score = models.IntegerField(default=0, help_text="Current score of the user.")
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        help_text="The team the user belongs to. Can be null if the user is not in a team."
    )
    # Add any other fields here if needed in the future, e.g., profile picture, bio, etc.

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['username'] # Or by score, depending on preferred default listing

    def __str__(self):
        return self.username
