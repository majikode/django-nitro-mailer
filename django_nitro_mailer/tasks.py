import logging
import os
import time
from django.db import transaction, models
from django.core.mail import get_connection
from typing import Optional
from django_nitro_mailer.models import Email, EmailLog

logger = logging.getLogger(__name__)

EMAIL_SEND_THROTTLE_MS = int(os.getenv("EMAIL_SEND_THROTTLE_MS", "1000"))


def throttle_email_delivery(throttle_delay: int) -> None:
    if throttle_delay > 0:
        logger.debug(f"Throttling email delivery. Sleeping for {throttle_delay} milliseconds")
        time.sleep(throttle_delay / 1000)


def send_emails(queryset: Optional[models.QuerySet] = None) -> None:
    if queryset is None:
        queryset = Email.objects.exclude(priority=Email.Priorities.DEFERRED).order_by("-priority", "created_at")

    connection = get_connection()

    with transaction.atomic():
        for email_obj in queryset.select_for_update(nowait=True):
            try:
                email_message = email_obj.email
                if email_message:
                    throttle_email_delivery(EMAIL_SEND_THROTTLE_MS)
                    connection.send_messages([email_message])

                    EmailLog.objects.create(email_data=email_obj.email_data, result=EmailLog.Results.SUCCESS)
                    email_obj.delete()
                else:
                    logger.error("Failed to retrieve email")

            except Exception as e:
                EmailLog.objects.create(email_data=email_obj.email_data, result=EmailLog.Results.FAILURE)
                logger.error("Failed to send email", exc_info=e)
