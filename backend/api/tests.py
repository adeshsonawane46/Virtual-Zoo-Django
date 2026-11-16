import json
from django.test import TestCase, Client
from api.models import User, Animal, QuizQuestion
from api.auth_utils import hash_password

class VirtualZooApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.animal = Animal.objects.create(
            id="m1",
            name="African Lion",
            category="MAMMAL",
            habitat="Savanna",
            region="Africa",
            diet="Carnivore",
            status="Vulnerable",
            desc="King of the jungle",
            image="http://example.com/lion.jpg",
            scientificName="Panthera leo",
            size="5 feet",
            lifespan="14 years",
            conservation="Protected",
            threats="Poaching"
        )
        self.quiz_q = QuizQuestion.objects.create(
            id="q1",
            question="Which animal is known as the king of the jungle?",
            options=["Lion", "Tiger", "Bear", "Elephant"],
            correctAnswer="Lion",
            category="MAMMAL",
            animal="African Lion"
        )

    def test_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"status": "ok"})

    def test_auth_and_user_flow(self):
        # 1. Register
        reg_res = self.client.post(
            "/api/auth/register",
            data=json.dumps({"name": "Test User", "email": "test@example.com", "password": "password123"}),
            content_type="application/json"
        )
        self.assertEqual(reg_res.status_code, 200)
        self.assertEqual(reg_res.json()["message"], "Registration successful")

        # Duplicate register
        dup_res = self.client.post(
            "/api/auth/register",
            data=json.dumps({"name": "Test User 2", "email": "test@example.com", "password": "password123"}),
            content_type="application/json"
        )
        self.assertEqual(dup_res.status_code, 409)

        # 2. Login
        login_res = self.client.post(
            "/api/auth/login",
            data=json.dumps({"email": "test@example.com", "password": "password123"}),
            content_type="application/json"
        )
        self.assertEqual(login_res.status_code, 200)
        token = login_res.json().get("token")
        self.assertIsNotNone(token)

        # 3. User Me
        auth_header = f"Bearer {token}"
        me_res = self.client.get("/api/user/me", HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(me_res.status_code, 200)
        self.assertEqual(me_res.json()["email"], "test@example.com")

        # 4. User Quiz Score
        score_res = self.client.post(
            "/api/user/quiz-score",
            data=json.dumps({"score": 9}),
            content_type="application/json",
            HTTP_AUTHORIZATION=auth_header
        )
        self.assertEqual(score_res.status_code, 200)
        self.assertEqual(score_res.json()["user"]["bestScore"], 9)

        # 5. Leaderboard
        lead_res = self.client.get("/api/user/leaderboard")
        self.assertEqual(lead_res.status_code, 200)
        self.assertTrue(len(lead_res.json()) >= 1)
        self.assertEqual(lead_res.json()[0]["bestScore"], 9)

        # 6. User Quiz Complete
        comp_res = self.client.post(
            "/api/user/quiz-complete",
            data=json.dumps({}),
            content_type="application/json",
            HTTP_AUTHORIZATION=auth_header
        )
        self.assertEqual(comp_res.status_code, 200)
        self.assertTrue(comp_res.json()["user"]["quizCompleted"])

    def test_animals_endpoints(self):
        # List all
        res = self.client.get("/api/animals")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0]["id"], "m1")

        # Filter category
        cat_res = self.client.get("/api/animals?category=MAMMAL")
        self.assertEqual(cat_res.status_code, 200)
        self.assertEqual(len(cat_res.json()), 1)

        # Detail
        det_res = self.client.get("/api/animals/m1")
        self.assertEqual(det_res.status_code, 200)
        self.assertEqual(det_res.json()["name"], "African Lion")

        # Not found
        nf_res = self.client.get("/api/animals/nonexistent")
        self.assertEqual(nf_res.status_code, 404)

    def test_quiz_endpoints(self):
        # Gemini quiz fallback
        res = self.client.get("/api/quiz/generate-gemini?animal=African%20Lion&category=MAMMAL")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["animal"], "African Lion")
        self.assertEqual(len(data["questions"]), 10)

        # Legacy quiz
        leg_res = self.client.get("/api/quiz?category=MAMMAL")
        self.assertEqual(leg_res.status_code, 200)
        self.assertTrue(len(leg_res.json()) >= 1)
