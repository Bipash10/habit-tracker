import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------- Security --------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "fallback-secret-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "") != "False"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

# -------------------- Apps --------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "habits",
    "django_crontab",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "habit_tracker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "habits" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "habit_tracker.wsgi.application"

# -------------------- Database --------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "habitdb"),
        "USER": os.environ.get("POSTGRES_USER", "habituser"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "bipash"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# -------------------- Static files --------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "habits" / "static"]

# -------------------- Auth --------------------
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

# -------------------- Cron Jobs --------------------
CRONJOBS = [
    ("0 0 * * *", "habits.cron.reset_habits_daily"),
]

# -------------------- Optional: Security for Production --------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")  # e.g., your Render URL

import dj_database_url

DATABASES['default'] = dj_database_url.config(
    default=os.environ.get("DATABASE_URL")
)
