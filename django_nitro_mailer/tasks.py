import logging
import os
from typing import Optional

import timezone
from django.core.mail import get_connection
from django.db import models, transaction

from django_nitro_mailer.models import Email, EmailLog

logger = logging.getLogger(__name__)
email_db_logging = os.getenv("EMAIL_DB_LOGGING_ENABLED", "true").lower() == "true"


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

                    if email_db_logging:
                        EmailLog.objects.create(email_data=email_obj.email_data, result=EmailLog.Results.SUCCESS)

                    logger.info(
                        "Email sent successfully",
                        extra={"recipients": email_obj.recipients, "created_at": timezone.now()},
                    )

                    email_obj.delete()

                else:
                    logger.error("Failed to retrieve email")

            except Exception as e:
                if email_db_logging:
                    EmailLog.objects.create(email_data=email_obj.email_data, result=EmailLog.Results.FAILURE)

                logger.error("Failed to send email", exc_info=e)
