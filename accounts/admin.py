from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'career_goal', 'experience_level', 'weekly_study_hours', 'preferred_platform')
    search_fields = ('user__username', 'career_goal')
    list_filter = ('experience_level',)
