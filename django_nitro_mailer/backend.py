import logging
from typing import Iterable
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage

from django_nitro_mailer.models import Email

logger = logging.getLogger(__name__)


class DatabaseBackend(BaseEmailBackend):
    def send_messages(self, email_messages: Iterable[EmailMessage]) -> int:
        email_list = []
        for email_obj in email_messages:
            email = Email()
            email.set_email(email_obj)
            email_list.append(email)

        email_db_list = Email.objects.bulk_create(email_list, batch_size=1000)
        return len(email_db_list)
