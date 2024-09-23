import logging
import os
from typing import Iterable
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage
from django.core.mail import get_connection as django_get_connection
from django.conf import settings


from django_nitro_mailer.models import Email, EmailLog
from django_nitro_mailer.tasks import throttle_email_delivery

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
    def get_connection(self, fail_silently=False):
        backend_path = settings.NITRO_MAILER_EMAIL_BACKEND
        return django_get_connection(backend_path, fail_silently=fail_silently)

    def send_messages(self, email_messages: Iterable[EmailMessage]) -> int:
        successful_sends = 0
        connection = self.get_connection()
        for email_message in email_messages:
            try:
                connection.send_messages([email_message])
                if email_db_logging:
                    EmailLog.objects.create(
                        email_data=email_message.message().as_bytes(), result=EmailLog.Results.SUCCESS
                    )
                logger.info(
                    "Email sent successfully", extra={"recipients": email_message.to, "subject": email_message.subject}
                )
                successful_sends += 1
            except Exception as e:
                if email_db_logging:
                    EmailLog.objects.create(
                        email_data=email_message.message().as_bytes(), result=EmailLog.Results.FAILURE
                    )
                logger.error(f"Failed to send email: {e}", exc_info=True)
            throttle_email_delivery()

        return successful_sends
