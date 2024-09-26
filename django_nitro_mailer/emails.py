import logging
from typing import Optional

from django.core.mail import get_connection
from django.db import models, transaction

from django_nitro_mailer.models import Email
from django_nitro_mailer.utils import send_email_message, throttle_email_delivery

logger = logging.getLogger(__name__)


def send_emails(queryset: Optional[models.QuerySet] = None) -> None:
    if queryset is None:
        queryset = Email.objects.exclude(priority=Email.Priorities.DEFERRED).order_by("-priority", "created_at")

    connection = get_connection()
    with transaction.atomic():
        for email_obj in queryset.select_for_update(nowait=True):
            try:
                email_message = email_obj.email
                if email_obj.email:
                    send_email_message(email_message, connection)
                    email_obj.delete()
                    throttle_email_delivery()
                else:
                    logger.error("No email message found for Email object: %s", email_obj.id, exc_info=True)

            except Exception as e:
                logger.error(
                    "Failed to send or delete email %s: %s",
                    email_obj.id,
                    str(e),
                    extra={"email_id": email_obj.id},
                    exc_info=True,
                )


def retry_deferred() -> None:
    deferred_emails = Email.objects.filter(priority=Email.Priorities.DEFERRED)
    if deferred_emails.exists():
        send_emails(deferred_emails)
