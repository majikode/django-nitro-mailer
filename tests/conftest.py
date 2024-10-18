import pytest
from django.conf import Settings


@pytest.fixture
def nitro_sync_backend_settings(settings: Settings) -> None:
    settings.EMAIL_BACKEND = "django_nitro_mailer.backends.SyncBackend"


@pytest.fixture
def nitro_database_backend_settings(settings: Settings) -> None:
    settings.EMAIL_BACKEND = "django_nitro_mailer.backends.DatabaseBackend"
