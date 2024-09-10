import pytest
from dev_settings import *


@pytest.fixture(autouse=True)
def django_test_settings(settings):

    settings.DATABASES["default"]["NAME"] = "test_nitro_mailer.db"
    if not settings.configured:
        settings.configure(
            DEBUG=DEBUG,
            SECRET_KEY=SECRET_KEY,
            DATABASES=DATABASES,
            INSTALLED_APPS=INSTALLED_APPS,
            ROOT_URLCONF=ROOT_URLCONF,
            MIDDLEWARE=MIDDLEWARE,
            TEMPLATES=TEMPLATES,
            STATIC_URL=STATIC_URL,
        )
