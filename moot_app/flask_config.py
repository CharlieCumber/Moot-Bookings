import os


class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SAMESITE="None"
    SESSION_COOKIE_SECURE=True
