import json
import random
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

from api.models import User, Animal, QuizQuestion
from api.auth_utils import hash_password, check_password, generate_jwt_token, require_auth
from api.gemini_service import generate_gemini_quiz
from api.sound_service import generate_sound

# ---------------- HEALTH CHECK ----------------
def health_check(request):
    return JsonResponse({"status": "ok"})


# ---------------- AUTH ROUTES ----------------
@csrf_exempt
def auth_register(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not name or not email or not password:
            return JsonResponse({"message": "All fields are required"}, status=400)

        if User.objects.filter(email__iexact=email).exists():
            return JsonResponse({"message": "Email already registered"}, status=409)

        hashed = hash_password(password)
        User.objects.create(name=name, email=email, password=hashed)

        return JsonResponse({"message": "Registration successful"}, status=200)
    except Exception as e:
        return JsonResponse({"message": "Registration failed", "error": str(e)}, status=500)


@csrf_exempt
def auth_login(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get("email", "").strip()
        password = data.get("password", "")

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return JsonResponse({"message": "User not found"}, status=400)

        if not check_password(password, user.password):
            return JsonResponse({"message": "Invalid password"}, status=400)

        token = generate_jwt_token(user.id)
        return JsonResponse({"token": token})
    except Exception as e:
        return JsonResponse({"message": "Login failed", "error": str(e)}, status=500)


@csrf_exempt
def auth_forgot_password(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get("email", "").strip()

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return JsonResponse({"message": "User not found"}, status=404)

        otp = str(random.randint(100000, 999999))
        user.reset_otp = otp
        user.otp_expiry = timezone.now() + timedelta(minutes=10)
        user.save()

        # Try to send email
        try:
            send_mail(
                subject="Virtual Zoo Password Reset OTP",
                message=f"Your OTP is {otp}",
                from_email=settings.EMAIL_HOST_USER or "noreply@virtualzoo.com",
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception as mail_err:
            print("Mail sending error:", mail_err)

        return JsonResponse({"message": "OTP sent to email"})
    except Exception as e:
        return JsonResponse({"message": "Could not send OTP", "error": str(e)}, status=500)


@csrf_exempt
def auth_reset_password(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get("email", "").strip()
        otp = str(data.get("otp", "")).strip()
        new_password = data.get("newPassword", "")

        user = User.objects.filter(email__iexact=email).first()
        if not user or str(user.reset_otp) != otp or not user.otp_expiry or user.otp_expiry < timezone.now():
            return JsonResponse({"message": "Invalid or expired OTP"}, status=400)

        user.password = hash_password(new_password)
        user.reset_otp = None
        user.otp_expiry = None
        user.save()

        return JsonResponse({"message": "Password reset successful"})
    except Exception as e:
        return JsonResponse({"message": "Password reset failed", "error": str(e)}, status=500)


# ---------------- USER ROUTES ----------------
def user_me(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    return require_auth(_user_me_inner)(request)

def _user_me_inner(request):
    return JsonResponse(request.user_obj.to_dict())


@csrf_exempt
def user_quiz_complete(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    return require_auth(_user_quiz_complete_inner)(request)

def _user_quiz_complete_inner(request):
    try:
        user = request.user_obj
        user.quiz_completed = True
        user.save()
        return JsonResponse({
            "message": "Quiz marked as completed",
            "user": user.to_dict()
        })
    except Exception as e:
        return JsonResponse({"message": "Could not update quiz status", "error": str(e)}, status=500)


@csrf_exempt
def user_quiz_score(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    return require_auth(_user_quiz_score_inner)(request)

def _user_quiz_score_inner(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        score = data.get("score")
        if not isinstance(score, (int, float)):
            return JsonResponse({"message": "Score must be a number"}, status=400)

        score = int(score)
        user = request.user_obj
        if not isinstance(user.scores, list):
            user.scores = []

        user.scores.append(score)
        user.last_score = score
        user.quizzes_taken = len(user.scores)
        user.best_score = max(user.best_score or 0, score)
        user.save()

        return JsonResponse({
            "message": "Score recorded",
            "user": user.to_dict()
        })
    except Exception as e:
        return JsonResponse({"message": "Could not record score", "error": str(e)}, status=500)


def user_leaderboard(request):
    try:
        users = User.objects.filter(best_score__gt=0).order_by('-best_score', '-quizzes_taken')[:20]
        results = [
            {
                "name": u.name,
                "email": u.email,
                "bestScore": u.best_score,
                "quizzesTaken": u.quizzes_taken,
                "lastScore": u.last_score
            }
            for u in users
        ]
        return JsonResponse(results, safe=False)
    except Exception as e:
        return JsonResponse({"message": "Could not fetch leaderboard", "error": str(e)}, status=500)


# ---------------- ANIMAL ROUTES ----------------
def animals_list(request):
    try:
        category = request.GET.get('category', '').strip()
        queryset = Animal.objects.all()
        if category:
            queryset = queryset.filter(category__iexact=category)

        animals = [a.to_dict() for a in queryset]
        return JsonResponse(animals, safe=False)
    except Exception as e:
        return JsonResponse([], safe=False)


def animal_detail(request, animal_id):
    try:
        animal = Animal.objects.filter(id__iexact=animal_id).first()
        if not animal:
            animal = Animal.objects.filter(name__iexact=animal_id).first()

        if not animal:
            return JsonResponse({"message": "Animal not found"}, status=404)

        return JsonResponse(animal.to_dict())
    except Exception as e:
        return JsonResponse({"message": "Failed to fetch animal"}, status=500)


# ---------------- QUIZ ROUTES ----------------
@csrf_exempt
def quiz_generate_gemini(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            animal = data.get("animal", "").strip()
            category = data.get("category", "").strip()
        else:
            animal = request.GET.get("animal", "").strip()
            category = request.GET.get("category", "").strip()

        if not animal:
            return JsonResponse({"message": "Animal parameter is required"}, status=400)

        mcqs = generate_gemini_quiz(animal, category)
        return JsonResponse({
            "animal": animal,
            "category": category,
            "questions": mcqs
        })
    except Exception as e:
        return JsonResponse({"message": "Failed to generate Gemini quiz", "error": str(e)}, status=500)


def quiz_legacy(request):
    try:
        category = request.GET.get("category", "").strip()
        animal = request.GET.get("animal", "").strip()

        if animal:
            mcqs = generate_gemini_quiz(animal, category)
            return JsonResponse(mcqs, safe=False)

        queryset = QuizQuestion.objects.all()
        if category:
            queryset = queryset.filter(category__iexact=category)

        questions = [q.to_dict() for q in queryset]
        return JsonResponse(questions, safe=False)
    except Exception as e:
        return JsonResponse({"message": "Quiz fetch error", "error": str(e)}, status=500)


# ---------------- SOUND ROUTE ----------------
@csrf_exempt
def sound_endpoint(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        prompt = data.get("prompt", "")
        return generate_sound(prompt)
    except Exception as e:
        return JsonResponse({"error": "Sound generation failed", "details": str(e)}, status=500)
