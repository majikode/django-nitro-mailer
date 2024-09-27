from django.conf import settings

NITRO_EMAIL_DATABASE_LOGGING = getattr(settings, "NITRO_EMAIL_DATABASE_LOGGING", True)
NITRO_EMAIL_BACKEND = getattr(settings, "NITRO_EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
