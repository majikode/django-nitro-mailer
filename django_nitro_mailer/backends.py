import logging
import os
from typing import Iterable
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage
from django.core.mail import get_connection as django_get_connection
from django.conf import settings


from django_nitro_mailer.models import Email, EmailLog
from django_nitro_mailer.tasks import throttle_email_delivery, send_email_message

logger = logging.getLogger(__name__)
email_db_logging = os.getenv("EMAIL_DB_LOGGING_ENABLED", "true").lower() == "true"


class DatabaseBackend(BaseEmailBackend):
    def send_messages(self, email_messages: Iterable[EmailMessage]) -> int:
        email_list = []
        for email_obj in email_messages:
            email = Email()
            email.set_email(email_obj)
            email_list.append(email)

        email_db_list = Email.objects.bulk_create(email_list, batch_size=1000)
        return len(email_db_list)


class SyncBackend(BaseEmailBackend):
    def get_connection(self, fail_silently: bool = False) -> int:
        backend_path = settings.NITRO_MAILER_EMAIL_BACKEND
        return django_get_connection(backend_path, fail_silently=fail_silently)

    def send_messages(self, email_messages: Iterable[EmailMessage]) -> int:
        successful_sends = 0
        connection = self.get_connection()
        for email_message in email_messages:
            if send_email_message(email_message, connection):
                successful_sends += 1
            throttle_email_delivery()

        return successful_sends
