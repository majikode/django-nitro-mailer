from django.db import transaction, models
from django.core.mail import get_connection
from typing import Optional
from django_nitro_mailer.models import Email, EmailLog


def send_emails(queryset: Optional[models.QuerySet] = None) -> None:
    if queryset is None:
        queryset = Email.objects.filter(priority__gt=0).order_by("-priority", "created_at")

    connection = get_connection()

    with transaction.atomic():
        for email in queryset:
            try:
                email_instance = email.email
                print(f"Email instance: {email_instance}")
                if email_instance:
                    success = connection.send_messages([email_instance])
                    if success:
                        EmailLog.objects.create(email_data=email.email_data, result=EmailLog.Results.SUCCESS)
                        email.delete()
                    else:
                        raise Exception("Email sending failed")
            except Exception as e:
                EmailLog.objects.create(email_data=email.email_data, result=EmailLog.Results.FAILURE)
                print(f"Failed to send email: {e}")
