import os
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from functools import wraps
from django.http import JsonResponse
from api.models import User

JWT_SECRET = os.getenv('JWT_SECRET', 'virtual-zoo-secret-key')

def hash_password(plain_password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against bcrypt hash."""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def generate_jwt_token(user_id: str | int) -> str:
    """Generate JWT token valid for 1 day matching Node.js jwt.sign."""
    payload = {
        'id': str(user_id),
        'exp': datetime.now(timezone.utc) + timedelta(days=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def decode_jwt_token(token: str) -> dict:
    """Decode and verify JWT token."""
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])

def require_auth(view_func):
    """
    Decorator for views requiring authentication via Bearer token.
    Mimics backend/middleware/auth.js:
    - 401: No token provided
    - 403: Invalid or expired token
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        parts = auth_header.split(' ')
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return JsonResponse({'message': 'No token provided'}, status=401)
        
        token = parts[1]
        try:
            decoded = decode_jwt_token(token)
            user_id = decoded.get('id')
            user = User.objects.filter(id=user_id).first()
            if not user:
                return JsonResponse({'message': 'User not found'}, status=404)
            request.user_obj = user
            request.user_id = user_id
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid or expired token'}, status=403)
        except Exception:
            return JsonResponse({'message': 'Invalid or expired token'}, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapped_view
