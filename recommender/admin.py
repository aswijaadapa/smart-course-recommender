from django.contrib import admin
from .models import SavedCourse, RecommendationHistory


@admin.register(SavedCourse)
class SavedCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'saved_at')
    list_filter = ('saved_at',)


@admin.register(RecommendationHistory)
class RecommendationHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'career_goal', 'created_at')
    list_filter = ('created_at',)
