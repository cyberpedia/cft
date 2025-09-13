# api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


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


class Tag(models.Model):
    """
    Represents a category or tag for challenges.
    """
    name = models.CharField(max_length=50, unique=True, help_text="Name of the tag/category (e.g., Web, Crypto).")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['name']

    def __str__(self):
        return self.name


class Challenge(models.Model):
    """
    Represents a CTF challenge.
    """
    name = models.CharField(max_length=255, unique=True, help_text="The name of the challenge.")
    description = models.TextField(help_text="Detailed description of the challenge.")
    points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Base points for solving this challenge. For dynamic challenges, this is the initial maximum points."
    )
    flag = models.CharField(max_length=255, unique=False, help_text="The flag string for this challenge.")
    tags = models.ManyToManyField(
        Tag,
        related_name='challenges',
        blank=True,
        help_text="Tags or categories associated with this challenge."
    )
    is_published = models.BooleanField(default=False, help_text="Whether the challenge is visible to players.")
    is_dynamic = models.BooleanField(default=False, help_text="True if this is a dynamic challenge (e.g., KoTH, AWD).")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_blood = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='first_bloods',
        help_text="The user who achieved 'First Blood' on this challenge."
    )
    # Potentially add fields for file attachments, hints, etc. later

    class Meta:
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"
        ordering = ['points', 'name']

    def __str__(self):
        return self.name


class Solve(models.Model):
    """
    Records a successful flag submission for a challenge by a user.
    Includes a UniqueConstraint to prevent duplicate solves.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solves', help_text="The user who solved the challenge.")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='solves', help_text="The challenge that was solved.")
    solved_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the challenge was solved.")
    points_awarded = models.IntegerField(null=True, blank=True, help_text="Points awarded at the time of solve (useful for dynamic scoring).")

    class Meta:
        verbose_name = "Solve"
        verbose_name_plural = "Solves"
        # Ensure a user can only solve a specific challenge once
        constraints = [
            models.UniqueConstraint(fields=['user', 'challenge'], name='unique_user_challenge_solve')
        ]
        ordering = ['-solved_at']

    def __str__(self):
        return f"{self.user.username} solved {self.challenge.name} at {self.solved_at.strftime('%Y-%m-%d %H:%M:%S')}"
