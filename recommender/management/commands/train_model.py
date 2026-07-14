from django.core.management.base import BaseCommand
from recommender.ml_engine import build_and_save_model


class Command(BaseCommand):
    help = "Trains the TF-IDF content-based recommendation model and saves it with joblib."

    def handle(self, *args, **options):
        count = build_and_save_model()
        self.stdout.write(self.style.SUCCESS(
            f"Model trained on {count} courses and saved to saved_model/"
        ))
