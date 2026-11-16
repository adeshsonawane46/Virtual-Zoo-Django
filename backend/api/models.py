from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    # Password reset fields
    reset_otp = models.CharField(max_length=20, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    
    # Quiz stats
    quiz_completed = models.BooleanField(default=False)
    scores = models.JSONField(default=list, blank=True)
    best_score = models.IntegerField(default=0)
    last_score = models.IntegerField(default=0)
    quizzes_taken = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "_id": str(self.id),
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "quizCompleted": self.quiz_completed,
            "scores": self.scores if isinstance(self.scores, list) else [],
            "bestScore": self.best_score,
            "lastScore": self.last_score,
            "quizzesTaken": self.quizzes_taken,
        }

    def __str__(self):
        return f"{self.name} ({self.email})"


class Animal(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, db_index=True)
    habitat = models.TextField(blank=True, default='')
    region = models.TextField(blank=True, default='')
    diet = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=100, blank=True, default='')
    desc = models.TextField(blank=True, default='')
    image = models.TextField(blank=True, default='')
    scientificName = models.CharField(max_length=255, blank=True, default='')
    size = models.CharField(max_length=100, blank=True, default='')
    lifespan = models.CharField(max_length=100, blank=True, default='')
    conservation = models.TextField(blank=True, default='')
    threats = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "habitat": self.habitat,
            "region": self.region,
            "diet": self.diet,
            "status": self.status,
            "desc": self.desc,
            "image": self.image,
            "scientificName": self.scientificName,
            "size": self.size,
            "lifespan": self.lifespan,
            "conservation": self.conservation,
            "threats": self.threats,
        }

    def __str__(self):
        return f"{self.name} ({self.category})"


class QuizQuestion(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    question = models.TextField()
    options = models.JSONField(default=list)
    correctAnswer = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    animal = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "options": self.options if isinstance(self.options, list) else [],
            "correctAnswer": self.correctAnswer,
            "category": self.category,
            "animal": self.animal,
        }

    def __str__(self):
        return f"{self.question[:50]}... ({self.animal})"
