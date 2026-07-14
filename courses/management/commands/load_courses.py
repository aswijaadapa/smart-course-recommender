import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from courses.models import Course


class Command(BaseCommand):
    help = "Loads courses from dataset/courses.csv into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help="Delete all existing courses before loading.",
        )

    def handle(self, *args, **options):
        csv_path = Path(settings.BASE_DIR) / 'dataset' / 'courses.csv'

        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"Dataset not found at {csv_path}"))
            return

        if options['clear']:
            deleted, _ = Course.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing course rows."))

        created_count = 0
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Course.objects.create(
                    course_name=row['course_name'],
                    platform=row['platform'],
                    category=row['category'],
                    career_domain=row['career_domain'],
                    skills_required=row['skills_required'],
                    tags=row['tags'],
                    difficulty=row['difficulty'],
                    duration=row['duration'],
                    rating=float(row['rating']),
                    description=row['description'],
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Loaded {created_count} courses into the database."))
