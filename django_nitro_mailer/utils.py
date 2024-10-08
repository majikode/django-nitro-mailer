import logging
import os
import time

from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage
from django.utils import timezone

from django_nitro_mailer.models import EmailLog
from django_nitro_mailer.settings import NITRO_EMAIL_DATABASE_LOGGING

logger = logging.getLogger(__name__)


def create_email_message(
    subject: str,
    recipients: list[str],
    text_content: str,
    html_content: str | None = None,
    from_email: str | None = None,
    attachments: list[str] | None = None,
) -> EmailMultiAlternatives:
    email = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=from_email, to=recipients, attachments=attachments
    )
    if html_content:
        email.attach_alternative(html_content, "text/html")

    return email


def send_email_message(email_data: EmailMessage, connection: BaseEmailBackend) -> bool:
    try:
        successful = bool(connection.send_messages([email_data]))

        if NITRO_EMAIL_DATABASE_LOGGING:
            EmailLog.log(email=email_data, result=EmailLog.Results.SUCCESS if successful else EmailLog.Results.FAILURE)

        logger.info(
            "Email sent successfully",
            extra={"recipients": email_data.recipients, "created_at": timezone.now()},
        )
    except Exception as e:
        if NITRO_EMAIL_DATABASE_LOGGING:
            EmailLog.log(email=email_data, result=EmailLog.Results.FAILURE)

        logger.exception("Failed to send email", exc_info=e)
        return False

    return successful


def throttle_email_delivery() -> None:
    throttle_delay = int(os.getenv("EMAIL_SEND_THROTTLE_MS", "0"))
    if throttle_delay > 0:
        logger.debug("Throttling email delivery. Sleeping for %d milliseconds", throttle_delay)
        time.sleep(throttle_delay / 1000)
