# api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        help_text="Current points for solving this challenge. Updates dynamically if dynamic scoring is enabled."
    )
    initial_points = models.IntegerField(
        default=500,
        validators=[MinValueValidator(0)],
        help_text="Starting points for this challenge (used in dynamic scoring)."
    )
    minimum_points = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0)],
        help_text="Minimum points this challenge can drop to (used in dynamic scoring)."
    )
    decay_factor = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        help_text="Points to deduct per solve for dynamic challenges. E.g., 10 points per solve."
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
    file = models.FileField(
        upload_to='challenge_files/',
        null=True,
        blank=True,
        help_text="Optional file attachment for the challenge."
    )
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

    class Meta:
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"
        ordering = ['points', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # For new challenges or when initial_points changes, update the current points.
        # For dynamic challenges, this is the starting point before decay.
        # For static challenges, this is its fixed point value.
        if not self.is_dynamic or self.pk is None: # If static OR new dynamic challenge
             self.points = self.initial_points
        # For existing dynamic challenges, the 'points' field is updated by solve logic.
        # An admin might manually reset 'points' to 'initial_points' if 'initial_points' or 'decay_factor' change.
        super().save(*args, **kwargs)


class Hint(models.Model):
    """
    Represents a hint for a specific challenge.
    Hints can have a cost associated with them.
    """
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
        related_name='hints',
        help_text="The challenge this hint belongs to."
    )
    text = models.TextField(help_text="The content of the hint.")
    cost = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Points required to unlock this hint. Default is 0 (free)."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hint"
        verbose_name_plural = "Hints"
        ordering = ['challenge', 'cost']

    def __str__(self):
        return f"Hint for '{self.challenge.name}' (Cost: {self.cost})"


class UnlockedHint(models.Model):
    """
    Tracks which users have unlocked which hints.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unlocked_hints', help_text="The user who unlocked the hint.")
    hint = models.ForeignKey(Hint, on_delete=models.CASCADE, related_name='unlocked_by', help_text="The hint that was unlocked.")
    unlocked_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the hint was unlocked.")

    class Meta:
        verbose_name = "Unlocked Hint"
        verbose_name_plural = "Unlocked Hints"
        # Ensure a user can only unlock a specific hint once
        constraints = [
            models.UniqueConstraint(fields=['user', 'hint'], name='unique_user_hint_unlock')
        ]
        ordering = ['-unlocked_at']

    def __str__(self):
        return f"{self.user.username} unlocked hint for '{self.hint.challenge.name}' (ID: {self.hint.id})"


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


class CTFSetting(models.Model):
    """
    Singleton model to store global CTF settings like scoring mode.
    Ensures only one instance of this model can exist.
    """
    SCORING_MODE_CHOICES = [
        ('static', 'Static Scoring'),
        ('dynamic', 'Dynamic Scoring'),
    ]
    scoring_mode = models.CharField(
        max_length=10,
        choices=SCORING_MODE_CHOICES,
        default='static',
        help_text="Defines how challenge points are awarded and updated."
    )
    # Add other global settings here as needed (e.g., event start/end times)

    class Meta:
        verbose_name = "CTF Setting"
        verbose_name_plural = "CTF Settings"

    def __str__(self):
        return "CTF Global Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance of CTFSetting exists
        if CTFSetting.objects.exists() and not self.pk:
            # If an instance already exists and we are trying to create a new one,
            # retrieve the existing one and update it instead.
            existing_setting = CTFSetting.objects.first()
            self.pk = existing_setting.pk
            # Update fields from the new instance to the existing one.
            existing_setting.scoring_mode = self.scoring_mode
            # ... update other fields as they are added
            super(CTFSetting, existing_setting).save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Loads the single CTFSetting instance, creating it if it doesn't exist.
        """
        obj, created = cls.objects.get_or_create(pk=1) # Always use pk=1 for singleton
        return obj


class WriteUp(models.Model):
    """
    Model for user-submitted challenge write-ups.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writeups', help_text="The user who submitted the write-up.")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='writeups', help_text="The challenge this write-up is for.")
    content = models.TextField(help_text="The detailed content of the write-up.")
    submitted_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the write-up was submitted.")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current review status of the write-up."
    )

    class Meta:
        verbose_name = "Write-Up"
        verbose_name_plural = "Write-Ups"
        ordering = ['-submitted_at']
        # Optionally add a unique constraint if a user can only submit one write-up per challenge
        # constraints = [
        #     models.UniqueConstraint(fields=['user', 'challenge'], name='unique_user_challenge_writeup')
        # ]

    def __str__(self):
        return f"Write-up for '{self.challenge.name}' by {self.user.username} - Status: {self.status}"
