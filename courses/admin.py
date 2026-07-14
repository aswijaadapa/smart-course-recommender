from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'platform', 'category', 'difficulty', 'rating', 'duration')
    list_filter = ('platform', 'category', 'difficulty')
    search_fields = ('course_name', 'skills_required', 'tags', 'description')
    ordering = ('-rating',)
