from django.db import models


class Course(models.Model):

    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    course_name = models.CharField(max_length=255)
    platform = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    career_domain = models.CharField(max_length=100)
    skills_required = models.TextField(help_text="Comma-separated skills")
    tags = models.TextField(help_text="Comma-separated keywords used for ML matching")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration = models.CharField(max_length=50)
    rating = models.FloatField()
    description = models.TextField()

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return self.course_name

    def combined_text(self):
        """
        Builds a single text blob combining the fields that matter for
        content-based similarity matching. Used by the ML engine to build
        the TF-IDF matrix, and kept here so the ML code and any future
        feature always use the exact same feature construction logic.
        """
        return " ".join([
            self.category,
            self.career_domain,
            self.skills_required,
            self.tags,
            self.difficulty,
            self.description,
        ])
