from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):

    EXPERIENCE_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_skills = models.TextField(blank=True, help_text="Comma-separated, e.g. Python, SQL")
    interests = models.TextField(blank=True, help_text="Comma-separated, e.g. AI, Web Development")
    career_goal = models.CharField(max_length=255, blank=True)
    experience_level = models.CharField(
        max_length=20, choices=EXPERIENCE_CHOICES, blank=True, default='Beginner'
    )
    weekly_study_hours = models.PositiveIntegerField(default=5)
    preferred_platform = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ensures a profile always exists even for users created before this
    # signal existed (e.g. via createsuperuser before app was wired up).
    if not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()
