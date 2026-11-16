from django.urls import re_path
from api import views

urlpatterns = [
    re_path(r'^health/?$', views.health_check, name='health_check'),
    
    # Auth
    re_path(r'^auth/register/?$', views.auth_register, name='auth_register'),
    re_path(r'^auth/login/?$', views.auth_login, name='auth_login'),
    re_path(r'^auth/forgot-password/?$', views.auth_forgot_password, name='auth_forgot_password'),
    re_path(r'^auth/reset-password/?$', views.auth_reset_password, name='auth_reset_password'),
    
    # User
    re_path(r'^user/me/?$', views.user_me, name='user_me'),
    re_path(r'^user/quiz-complete/?$', views.user_quiz_complete, name='user_quiz_complete'),
    re_path(r'^user/quiz-score/?$', views.user_quiz_score, name='user_quiz_score'),
    re_path(r'^user/leaderboard/?$', views.user_leaderboard, name='user_leaderboard'),
    
    # Animals
    re_path(r'^animals/?$', views.animals_list, name='animals_list'),
    re_path(r'^animals/(?P<animal_id>[^/]+)/?$', views.animal_detail, name='animal_detail'),
    
    # Quiz
    re_path(r'^quiz/generate-gemini/?$', views.quiz_generate_gemini, name='quiz_generate_gemini'),
    re_path(r'^quiz/?$', views.quiz_legacy, name='quiz_legacy'),
    
    # Sound
    re_path(r'^sound/?$', views.sound_endpoint, name='sound_endpoint'),
]
