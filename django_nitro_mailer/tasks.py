import os
import logging
import timezone
from django.db import transaction, models
from django.core.mail import get_connection
from typing import Optional
from django_nitro_mailer.models import Email, EmailLog

logger = logging.getLogger(__name__)
email_logging_enabled = os.getenv("EMAIL_LOGGING_ENABLED", "false").lower() == "true"


def send_emails(queryset: Optional[models.QuerySet] = None) -> None:
    if queryset is None:
        queryset = Email.objects.exclude(priority=Email.Priorities.DEFERRED).order_by("-priority", "created_at")

    connection = get_connection()

    with transaction.atomic():
        for email_obj in queryset.select_for_update(nowait=True):
            try:
                email_message = email_obj.email
                if email_message:
                    connection.send_messages([email_message])
                    if email_logging_enabled:
                        EmailLog.objects.create(email_data=email_obj.email_data, result=EmailLog.Results.SUCCESS)
                        logger.info(
                            "Email sent successfully",
                            extra={"recipients": email_obj.recipients, "created_at": timezone.now()},
                        )
                    email_obj.delete()

                else:
                    logger.error("Failed to retrieve email")

            except Exception as e:
                EmailLog.objects.create(email_data=email_obj.email_data, result=EmailLog.Results.FAILURE)
                logger.error("Failed to send email", exc_info=e)
