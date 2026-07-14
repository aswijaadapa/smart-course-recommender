from django.db import models
from django.contrib.auth.models import User
from courses.models import Course


class SavedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.course.course_name}"


class RecommendationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_history')
    query_text = models.TextField(help_text="The combined profile text used to generate this recommendation")
    career_goal = models.CharField(max_length=255, blank=True)
    recommended_courses = models.ManyToManyField(Course, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Recommendation histories"

    def __str__(self):
        return f"{self.user.username} - {self.created_at:%Y-%m-%d %H:%M}"
