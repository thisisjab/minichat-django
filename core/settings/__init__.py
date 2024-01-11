"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
env.read_env(BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("PROJECT_DEBUG", default=False)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "dont__use__this__in__production" if DEBUG else env("PROJECT_SECRET_KEY")


ALLOWED_HOSTS = env.list("PROJECT_ALLOWED_HOSTS", default=[])


# Application definition

LOCAL_APPS = []

DEBUGGING_APPS = [
    "debug_toolbar",
]

THIRDPARTY_APPS = []

INSTALLED_APPS = (
    [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]
    + THIRDPARTY_APPS
    + LOCAL_APPS
)

if DEBUG:
    INSTALLED_APPS += DEBUGGING_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

DEFAULT_INTERNAL_IPS = ["127.0.0.1"]

if DEBUG:
    import socket

    # WARN: do not use `_` as variable name because it will be confused with gettext_lazy.
    hostname, __, ips = socket.gethostbyname_ex(socket.gethostname())
    DEFAULT_INTERNAL_IPS.extend(
        [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["10.0.2.2"]
    )

EXTRA_INTERNAL_IPS = env.list(
    var="PROJECT_EXTRA_INTERNAL_IPS", cast=str, default=list()
)

INTERNAL_IPS = (
    env.list(var="PROJECT_INTERNAL_IPS", cast=str, default=DEFAULT_INTERNAL_IPS)
    + EXTRA_INTERNAL_IPS
)


ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates"],
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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("PROJECT_POSTGRES_DB"),
        "USER": env("PROJECT_POSTGRES_USER"),
        "PASSWORD": env("PROJECT_POSTGRES_PASSWORD"),
        "HOST": env("PROJECT_POSTGRES_HOST", default="db"),
        "PORT": env("PROJECT_POSTGRES_PORT", default="5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "core/static/"
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
