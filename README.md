🦁 Virtual Zoo

An interactive full-stack Virtual Zoo web application where users can explore animals, view detailed information, authenticate securely, and take AI-generated quizzes powered by Google Gemini. The application also provides AI-generated animal sounds using ElevenLabs.

✨ Features

🐾 Browse animals by category

🔎 Search animals

📖 View detailed animal profiles

🌍 View habitat, diet, region, lifespan, and conservation status

🔐 User registration and login

🔑 JWT-based authentication

📧 Forgot password and password reset

🧠 AI-generated 10-question quizzes using Google Gemini

📝 Multiple-choice questions with explanations

🎯 Quiz score tracking

🏆 Leaderboard

🔊 AI-generated animal sounds using ElevenLabs

🖼️ Animal image fallback handling

📱 Responsive user interface

🗄️ SQLite database with Django ORM

🔄 Dynamic fallback quiz generation when Gemini is unavailable

🛠️ Tech Stack

Frontend

React.js

Vite

React Router

Axios

Tailwind CSS

Backend

Python 3.12

Django 5.1

Django REST Framework

Django CORS Headers

PyJWT (JWT Authentication)

bcrypt

SQLite / Django ORM

APIs & Services

Google Gemini API — AI quiz generation

ElevenLabs API — animal sound generation

📁 Project Structure

Virtual-Zoo/
│
├── backend/
│   ├── api/
│   │   ├── migrations/
│   │   ├── management/commands/seed_animals.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── auth_utils.py
│   │   ├── gemini_service.py
│   │   ├── sound_service.py
│   │   └── tests.py
│   ├── zoo_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── venv/
│   ├── animals_data.json
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── utils/
│   │   └── ...
│   ├── package.json
│   └── .env
│
└── README.md

The sound API and Gemini AI quiz generation are integrated into the Django backend API.

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/adeshsonawane46/virtual-zoo.git
cd virtual-zoo

⚙️ Backend Setup (Django + venv)

cd backend

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (Command Prompt):
venv\Scripts\activate.bat
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed animals dataset (126 animals)
python manage.py seed_animals

# Start Django development server on port 5001
python manage.py runserver 5001

Backend:
http://localhost:5001

> Alternatively, to run directly from the project root:
> ```powershell
> .\venv\Scripts\Activate.ps1
> python backend\manage.py runserver 5001
> ```

🎨 Frontend Setup

Open another terminal:

cd frontend
npm install

Create a .env file:

VITE_API_URL=http://localhost:5001
VITE_GOOGLE_CLIENT_ID=your_google_client_id

Start the frontend:

npm run dev

Frontend:

http://localhost:5173

🧠 AI Quiz System

The application uses the Google Gemini API to dynamically generate educational 10-question multiple-choice quizzes based on the selected animal.

Example:

GET /api/quiz/generate-gemini?animal=Lion&category=MAMMAL

Each generated question contains:

Question

Four options

Correct answer

Explanation

If the Gemini API is unavailable, the backend uses a dynamic fallback quiz generator.

🔊 AI Animal Sound Generation

Animal sounds are generated using the ElevenLabs Sound Effects API.

The sound route is part of the main Django backend:

POST /api/sound

Example request:

{
  "prompt": "Lion animal sound"
}

The backend securely communicates with ElevenLabs using the ELEVENLABS_API_KEY environment variable.

The ElevenLabs API key must never be placed in the React frontend or committed to GitHub.

🔐 Authentication

The application provides:

User registration

User login

JWT authentication

Forgot password

Password reset

Protected user features

Quiz score tracking

Leaderboard

The frontend automatically attaches the JWT token to authenticated API requests through an Axios interceptor.

🐾 Animal System

Users can browse animals by category and view individual animal profiles.

Get all animals

GET /api/animals

Get animals by category

GET /api/animals?category=MAMMAL

Get animal by ID

GET /api/animals/:id

Animal information can include:

Name

Scientific name

Description

Image

Category

Habitat

Diet

Size

Lifespan

Region

Conservation status

Primary threats

The backend also includes a static animal dataset that can act as a fallback when the database is unavailable or contains no matching animals.

📡 API Endpoints

Health

GET /api/health

Response:

{
  "status": "ok"
}

Animals

GET /api/animals
GET /api/animals/:id

Authentication

POST /api/auth/register
POST /api/auth/login
POST /api/auth/forgot-password
POST /api/auth/reset-password

Quiz

GET /api/quiz
GET /api/quiz/generate-gemini
POST /api/quiz/generate-gemini

User

POST /api/user/quiz-score
GET /api/user/leaderboard

Sound

POST /api/sound

🔑 Environment Variables

Backend (.env)

PORT=5001
SECRET_KEY=your_django_secret_key
DEBUG=True
JWT_SECRET=your_jwt_secret
EMAIL=your_email@gmail.com
EMAIL_PASS=your_email_app_password
GEMINI_API_KEY=your_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
FRONTEND_URL=http://localhost:5173

Frontend (.env)

VITE_API_URL=http://localhost:5001
VITE_GOOGLE_CLIENT_ID=your_google_client_id

Security

Never commit actual .env files or credentials to GitHub.

Never expose:

Django secret keys

JWT secrets

Gemini API keys

ElevenLabs API keys

Email app passwords

OAuth credentials

Use .env.example files to document required variables without exposing their values.

🌐 Production Deployment

Frontend — Vercel

Deploy the frontend directory to Vercel.

Add these production environment variables:

VITE_API_URL=https://virtual-zoo-backend-8xmc.onrender.com
VITE_GOOGLE_CLIENT_ID=your_google_client_id

After changing VITE_* environment variables, redeploy the frontend so the values are included in the Vite production build.

Backend — Render / Railway / PythonAnywhere

Deploy the backend directory as a Python Web Service.

Build command:

pip install -r requirements.txt && python manage.py migrate

Start command:

python manage.py runserver 0.0.0.0:$PORT

Add these environment variables:

PORT=5001
SECRET_KEY=your_production_django_secret_key
DEBUG=False
JWT_SECRET=your_jwt_secret
EMAIL=your_email@gmail.com
EMAIL_PASS=your_email_password
GEMINI_API_KEY=your_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
FRONTEND_URL=https://virtual-zoo-view.vercel.app

The Django backend handles animal data, authentication, user stats, Gemini quizzes, and ElevenLabs sound generation.

🗄️ Database (SQLite & Django ORM)

The application uses SQLite (`db.sqlite3`) managed through the Django ORM.

Database migrations and initial data seeding:

python manage.py migrate
python manage.py seed_animals

All 126 animal profiles are loaded from `animals_data.json` into the SQLite database.

🔒 CORS

The backend supports local development origins and the production frontend configured through:

FRONTEND_URL=https://virtual-zoo-view.vercel.app

This keeps the production frontend URL configurable through environment variables.

🩺 Health Check

After deploying the backend to Render, test:

https://virtual-zoo-backend-8xmc.onrender.com/api/health

Expected response:

{
  "status": "ok"
}

🧪 Local Development

Run the two applications separately.

Terminal 1 — Backend (Django)

cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver 5001

Terminal 2 — Frontend

cd frontend
npm install
npm run dev

Local architecture:

React Frontend
      │
      ▼
Django Backend :5001
      │
      ├── SQLite (db.sqlite3)
      ├── Gemini API
      └── ElevenLabs API

🌍 Production Architecture

                    ┌─────────────────────┐
                    │   Vercel Frontend   │
                    │      React + Vite   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Render Backend    │
                    │    Python + Django   │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       SQLite DB         Gemini API       ElevenLabs

📱 Responsive Design

The application is designed to work across:

Desktop

Laptop

Tablet

Mobile devices

🛡️ Security Practices

The project uses:

Environment variables for sensitive credentials

JWT-based authentication

Password hashing

CORS configuration

Backend-only API keys

.env files excluded from Git

Production API URLs configured through environment variables

📌 Important Notes

Gemini API keys must remain on the backend.

ElevenLabs API keys must remain on the backend.

Django secret key and API credentials must remain in environment variables.

Frontend VITE_* variables are exposed to the browser, so private API keys must never be placed in them.

After changing Vercel environment variables, redeploy the frontend.

After changing Render environment variables, redeploy the backend.

📄 License

This project is developed for educational and development purposes.

👨‍💻 Author

Adesh Sonawane

GitHub: https://github.com/adeshsonawane46