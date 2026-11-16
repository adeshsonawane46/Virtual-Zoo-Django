import os
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from api.models import Animal, QuizQuestion

class Command(BaseCommand):
    help = "Seed animals and sample quiz questions from animals_data.json"

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        json_path = base_dir / "animals_data.json"

        if not json_path.exists():
            # Try parent directory
            json_path = base_dir.parent / "animals_data.json"

        if not json_path.exists():
            self.stdout.write(self.style.ERROR(f"Could not find animals_data.json at {json_path}"))
            return

        with open(json_path, "r", encoding="utf-8") as f:
            animals_data = json.load(f)

        self.stdout.write(f"Loaded {len(animals_data)} animals from JSON. Seeding database...")

        created_count = 0
        updated_count = 0

        for a in animals_data:
            obj, created = Animal.objects.update_or_create(
                id=a.get("id"),
                defaults={
                    "name": a.get("name", ""),
                    "category": a.get("category", ""),
                    "habitat": a.get("habitat", ""),
                    "region": a.get("region", ""),
                    "diet": a.get("diet", ""),
                    "status": a.get("status", ""),
                    "desc": a.get("desc", ""),
                    "image": a.get("image", ""),
                    "scientificName": a.get("scientificName", ""),
                    "size": a.get("size", ""),
                    "lifespan": a.get("lifespan", ""),
                    "conservation": a.get("conservation", ""),
                    "threats": a.get("threats", "")
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded animals: {created_count} created, {updated_count} updated (Total: {len(animals_data)})"
        ))

        # Seed sample quiz question
        QuizQuestion.objects.update_or_create(
            id="q1",
            defaults={
                "question": "Which animal is known as the king of the jungle?",
                "options": ["Lion", "Tiger", "Bear", "Elephant"],
                "correctAnswer": "Lion",
                "category": "MAMMAL",
                "animal": "African Lion"
            }
        )
        self.stdout.write(self.style.SUCCESS("Sample quiz question seeded successfully."))
