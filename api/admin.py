# api/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db import transaction
from django.contrib import messages

from .models import User, Team, Tag, Challenge, Hint, UnlockedHint, Solve, CTFSetting, WriteUp, ContentPage


# Register Team model
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


# Register User model
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'score', 'team')
    # Fields to make searchable
    search_fields = ('username', 'email', 'team__name')
    # Fields to filter by
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'team')
    # Fields to edit on the detail page
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('score', 'team')}),
    )
    # Fields to add when creating a new user in the admin
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('score', 'team')}),
    )


# Register Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


class HintInline(admin.TabularInline):
    """
    Inline admin for Hints, allowing them to be managed directly within the Challenge admin.
    """
    model = Hint
    extra = 1 # Number of empty forms to display


# Register Challenge model
@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'is_published', 'is_dynamic', 'initial_points', 'minimum_points', 'decay_factor', 'first_blood', 'created_at', 'updated_at')
    list_filter = ('is_published', 'is_dynamic', 'tags')
    search_fields = ('name', 'description', 'flag')
    filter_horizontal = ('tags',)
    inlines = [HintInline] # Add HintInline to ChallengeAdmin
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'flag', 'file', 'tags', 'is_published', 'is_dynamic')
        }),
        ('Scoring', {
            'fields': ('initial_points', 'minimum_points', 'decay_factor', 'points'),
            'description': 'For dynamic challenges, "Points" will be updated automatically by solves. For static challenges, "Points" should be set to "Initial Points".'
        }),
        ('Meta Information', {
            'fields': ('first_blood', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('points', 'created_at', 'updated_at', 'first_blood') # 'points' is dynamically updated


# Register Hint model
@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'text', 'cost', 'created_at')
    list_filter = ('challenge',)
    search_fields = ('text', 'challenge__name')


# Register UnlockedHint model
@admin.register(UnlockedHint)
class UnlockedHintAdmin(admin.ModelAdmin):
    list_display = ('user', 'hint', 'unlocked_at')
    list_filter = ('user', 'hint__challenge')
    search_fields = ('user__username', 'hint__challenge__name', 'hint__text')
    readonly_fields = ('unlocked_at',)


# Register Solve model
@admin.register(Solve)
class SolveAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'solved_at', 'points_awarded')
    list_filter = ('solved_at', 'challenge', 'user')
    search_fields = ('user__username', 'challenge__name')
    readonly_fields = ('solved_at', 'points_awarded') # Typically solved_at and points_awarded are set programmatically


# Register CTFSetting model
@admin.register(CTFSetting)
class CTFSettingAdmin(admin.ModelAdmin):
    list_display = ('scoring_mode',)
    # Prevent adding new instances, only allow changing the existing one
    def has_add_permission(self, request):
        return not CTFSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False # Prevent deletion


@admin.register(WriteUp)
class WriteUpAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'user', 'status', 'submitted_at')
    list_filter = ('status', 'challenge', 'user')
    search_fields = ('challenge__name', 'user__username', 'content')
    actions = ['approve_writeups']

    def approve_writeups(self, request, queryset):
        """
        Admin action to approve selected pending write-ups and award bonus points.
        """
        # Define bonus points for write-ups
        BONUS_POINTS_FOR_WRITEUP = 50
        
        with transaction.atomic():
            approved_count = 0
            for writeup in queryset.filter(status='pending'):
                writeup.status = 'approved'
                writeup.save()
                
                # Award bonus points to the user
                user = writeup.user
                user.score += BONUS_POINTS_FOR_WRITEUP
                user.save()
                approved_count += 1
            
            if approved_count > 0:
                self.message_user(
                    request,
                    f"{approved_count} write-up(s) approved and {BONUS_POINTS_FOR_WRITEUP} bonus points awarded to each user.",
                    messages.SUCCESS
                )
            else:
                self.message_user(
                    request,
                    "No pending write-ups were selected or approved.",
                    messages.WARNING
                )
    approve_writeups.short_description = "Approve selected write-ups and award bonus points"


@admin.register(ContentPage)
class ContentPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'slug')
    prepopulated_fields = {'slug': ('title',)} # Automatically populate slug from title
