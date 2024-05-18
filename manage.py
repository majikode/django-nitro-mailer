#!/usr/bin/env python

"""
manage.py script used by django-nitro-mailer developers to create
DB migrations, test management commands and serve the admin page.
"""

DEFAULT_SETTINGS = {
    "DEBUG": True,
    "SECRET_KEY": "open-secret",
    "INSTALLED_APPS": [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django_nitro_mailer",
    ],
    "DATABASES": {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "nitro_mailer.db",
        }
    },
    "ROOT_URLCONF": "urls",
    "MIDDLEWARE": [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ],
    "TEMPLATES": [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
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
    ],
    "STATIC_URL": "/static/",
}

if __name__ == "__main__":
    from django.conf import settings
    from django.core import management

    settings.configure(**DEFAULT_SETTINGS)
    management.execute_from_command_line()
