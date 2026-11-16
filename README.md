# 🦁 Virtual Zoo

**Virtual Zoo** is an interactive full-stack web application designed to make wildlife education more accessible. Users can explore animal profiles, test their knowledge through AI-generated quizzes, listen to AI-generated animal sounds, and experience famous zoos through embedded 360-degree virtual tours.

This project was developed as part of **INT253 – Web Development in Python using Django**.

## ✨ Features

### Animal Explorer
- Browse animals across six categories: Mammal, Bird, Fish, Reptile, Amphibian, and Insect.
- Search and explore animal profiles.
- View scientific name, description, habitat, diet, size, lifespan, region, conservation status, and primary threats.
- Fallback images when animal images cannot be loaded.
- Static animal dataset fallback.

### AI Quiz
- Select a quiz category and animal.
- Generate 10-question multiple-choice quizzes using Google Gemini API.
- Four options, correct answers, and explanations.
- Dynamic fallback quiz generation when Gemini is unavailable.
- Save quiz scores for logged-in users.
- Dashboard statistics and leaderboard.

### 360-Degree Virtual Tour
- Browse and search seven famous zoos:
  - London Zoo
  - Singapore Zoo
  - Bronx Zoo
  - San Diego Zoo
  - Taronga Zoo Sydney
  - Toronto Zoo
  - Berlin Zoo
- Embedded interactive 360-degree street-level walkthroughs.
- Look around, navigate panorama points, zoom, and use full-screen mode.

### Authentication and Other Features
- User registration and login.
- JWT-based authentication.
- Password hashing using bcrypt.
- Forgot password and password reset.
- User dashboard and leaderboard.
- AI-generated animal sounds using ElevenLabs.
- Responsive user interface.

## 🛠️ Technology Stack

### Frontend
- React.js
- Vite
- React Router
- Axios
- Tailwind CSS

### Backend
- Python 3.12
- Django 5.1
- Django REST Framework
- Django CORS Headers
- PyJWT
- bcrypt

### Database
- SQLite
- Django ORM

### APIs and Services
- Google Gemini API – AI quiz generation.
- ElevenLabs API – AI animal sound generation.

## 🧩 My Contribution

My individual contribution covered the **Quiz page and Virtual Tour page**, including frontend and backend development.

### Quiz Page
- Developed the category selection, animal selection, and quiz interfaces using React.js.
- Implemented a 10-question multiple-choice quiz interface.
- Integrated the frontend with Django REST API endpoints.
- Developed Django views and URL routes for quiz generation and retrieval.
- Integrated Google Gemini API through `gemini_service.py`.
- Implemented dynamic fallback quiz generation.
- Developed quiz score submission and leaderboard functionality.
- Integrated JWT authentication for protected API requests.
- Tested the complete quiz workflow.

### Virtual Tour Page
- Developed the Virtual Zoo Tours listing page.
- Added seven famous zoos with images, descriptions, and Start Tour functionality.
- Implemented zoo search functionality.
- Developed the interactive 360-degree tour viewer.
- Integrated embedded street-level views.
- Supported panorama navigation, zoom, compass, and full-screen functionality.
- Developed responsive layouts for different screen sizes.

**Implementation Note:** The zoo list and tour links are defined in the React frontend. The project does not describe a dedicated Django REST endpoint for tour data.

## 🏗️ Application Architecture

The application follows a three-tier architecture:

1. **React Frontend:** Handles the user interface and API requests using Axios.
2. **Django Backend:** Handles REST APIs, authentication, quiz generation, and application logic.
3. **SQLite Database:** Stores application data using Django ORM.

### AI Quiz Workflow

1. User selects a category and animal.
2. React sends a request to the Django backend.
3. Django communicates with Google Gemini.
4. Gemini generates 10 multiple-choice questions.
5. Backend validates the generated response.
6. A fallback generator is used if Gemini is unavailable.
7. User submits the quiz.
8. Django saves the score and updates leaderboard data.

## 📁 Project Structure

```text
Virtual-Zoo-Django/
│
├── backend/
│   ├── api/
│   │   ├── migrations/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── seed_animals.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── auth_utils.py
│   │   ├── gemini_service.py
│   │   ├── sound_service.py
│   │   └── tests.py
│   │
│   ├── zoo_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── animals_data.json
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── utils/
│   ├── package.json
│   └── .env.example
│
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/adeshsonawane46/Virtual-Zoo-Django.git

cd Virtual-Zoo-Django
```

### 2. Backend Setup

```bash
cd backend

python -m venv venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
venv\Scripts\activate.bat
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the backend directory:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
PORT=5001
JWT_SECRET=your_jwt_secret
GEMINI_API_KEY=your_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
FRONTEND_URL=http://localhost:5173
```

Apply migrations:

```bash
python manage.py migrate
```

Load animal dataset:

```bash
python manage.py seed_animals
```

Start Django server:

```bash
python manage.py runserver 5001
```

Backend URL:

```text
http://localhost:5001
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend

npm install
```

Create a `.env` file:

```env
VITE_API_URL=http://localhost:5001
VITE_GOOGLE_CLIENT_ID=your_google_client_id
```

Start the frontend:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## 📡 API Endpoints

### Health
```http
GET /api/health
```

### Animals
```http
GET /api/animals
GET /api/animals/{id}
```

### Authentication
```http
POST /api/auth/register
POST /api/auth/login
POST /api/auth/forgot-password
POST /api/auth/reset-password
```

### Quiz
```http
GET /api/quiz
GET /api/quiz/generate-gemini
POST /api/quiz/generate-gemini
```

### User
```http
POST /api/user/quiz-score
GET /api/user/leaderboard
```

### Sound
```http
POST /api/sound
```

### Example: Generate AI Quiz

```http
GET /api/quiz/generate-gemini?animal=Lion&category=MAMMAL
```

Each generated question includes:
- Question
- Four options
- Correct answer
- Explanation

### Example: Generate Animal Sound

```http
POST /api/sound
Content-Type: application/json
```

```json
{
  "prompt": "Lion animal sound"
}
```

## 🗄️ Database

The application uses SQLite with Django ORM.

Database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

The project includes `animals_data.json` and a Django management command to load the animal dataset.

The project report describes 126 animal profiles across six categories.

## 🔐 Security Practices

- Environment variables for sensitive credentials.
- JWT-based authentication.
- Password hashing using bcrypt.
- CORS configuration.
- Backend-only API keys.
- `.env` files excluded from Git.
- Protected API requests using JWT authentication.

**Important:** Never expose Django secret keys, JWT secrets, Gemini API keys, ElevenLabs API keys, or email credentials in frontend code or public repositories.

## 🧪 Testing

Run backend tests:

```bash
cd backend

python manage.py test
```

Recommended manual testing:

1. Select a quiz category.
2. Choose an animal.
3. Generate and answer all ten questions.
4. Submit the quiz.
5. Verify the score on the dashboard and leaderboard.
6. Search for zoos on the Virtual Tour page.
7. Open and test the 360-degree tour functionality.

## 🔮 Future Improvements

- Migrate SQLite to PostgreSQL.
- Add quiz history and advanced analytics.
- Add difficulty levels and quiz timers.
- Create a dedicated Django API and admin panel for zoo tours.
- Add more zoos and wildlife parks.
- Introduce multilingual support.
- Expand automated testing and CI/CD integration.

## 📄 License

This project is developed for educational and development purposes.

## 👨‍💻 Author

**Adesh Sonawane**

GitHub: [adeshsonawane46](https://github.com/adeshsonawane46)

## 🔗 Project Repository

[Virtual Zoo – Django GitHub Repository](https://github.com/adeshsonawane46/Virtual-Zoo-Django.git)
