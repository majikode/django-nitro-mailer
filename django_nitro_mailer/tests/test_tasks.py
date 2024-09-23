import pytest
import pickle
from unittest.mock import patch, MagicMock
from django.conf import settings
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django_nitro_mailer.tasks import send_emails
from django_nitro_mailer.models import Email, EmailLog
from django_nitro_mailer.backend import SyncBackend


@pytest.mark.django_db
def test_set_and_get_email() -> None:
    email_instance = Email.objects.create(email_data=b"")

    email_message = EmailMessage(
        subject="Test Subject", body="Test Body", from_email="from@example.com", to=["to@example.com"]
    )

    email_instance.set_email(email_message)

    assert email_instance.email.subject == "Test Subject"
    assert email_instance.email.body == "Test Body"
    assert email_instance.recipients == ["to@example.com"]


@pytest.mark.django_db
def test_send_emails_success_console() -> None:

    settings.EMAIL_BACKEND = "django_nitro_mailer.backend.DatabaseBackend"
    settings.NITRO_MAILER_EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    send_mail(
        subject="Test Subject",
        message="Test message body",
        from_email="from@example.com",
        recipient_list=["to@example.com"],
        fail_silently=False,
    )

    assert Email.objects.count() == 1
    assert EmailLog.objects.count() == 0

    send_emails()

    assert EmailLog.objects.count() == 1

    email_log = EmailLog.objects.first()
    assert email_log.result == EmailLog.Results.SUCCESS


@pytest.mark.django_db
def test_send_emails_success_smtp() -> None:
    settings.EMAIL_BACKEND = "django_nitro_mailer.backend.DatabaseBackend"
    settings.NITRO_MAILER_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    send_mail(
        subject="Test Subject",
        message="Test Body",
        from_email="from@example.com",
        recipient_list=["to@example.com"],
        fail_silently=False,
    )

    assert Email.objects.count() == 1
    assert EmailLog.objects.count() == 0

    send_emails()

    assert EmailLog.objects.count() == 1

    email_log = EmailLog.objects.first()
    assert email_log.result == EmailLog.Results.SUCCESS


@pytest.mark.django_db
@patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
def test_send_emails_with_priorities(mock_send_messages: MagicMock):
    mock_send_messages.return_value = 1

    high_priority_email = EmailMessage(
        subject="High Priority", body="Test Body", from_email="from@example.com", to=["to@example.com"]
    )
    medium_priority_email = EmailMessage(
        subject="Medium Priority", body="Test Body", from_email="from@example.com", to=["to@example.com"]
    )
    low_priority_email = EmailMessage(
        subject="Low Priority", body="Test Body", from_email="from@example.com", to=["to@example.com"]
    )
    medium_priority_email_2 = EmailMessage(
        subject="Medium Priority", body="Test Body", from_email="from@example.com", to=["to@example.com"]
    )
    low_priority_email_2 = EmailMessage(
        subject="Low Priority", body="Test Body", from_email="from@example.com", to=["to@example.com"]
    )
    deferred_priority_email = EmailMessage(
        subject="Deferred Priority", body="Test Body", from_email="from@example.com", to=["to@example.com"]
    )

    Email.objects.create(email_data=pickle.dumps(high_priority_email), priority=Email.Priorities.HIGH)
    Email.objects.create(email_data=pickle.dumps(medium_priority_email), priority=Email.Priorities.MEDIUM)
    Email.objects.create(email_data=pickle.dumps(low_priority_email), priority=Email.Priorities.LOW)
    Email.objects.create(email_data=pickle.dumps(medium_priority_email_2), priority=Email.Priorities.MEDIUM)
    Email.objects.create(email_data=pickle.dumps(low_priority_email_2), priority=Email.Priorities.LOW)
    Email.objects.create(email_data=pickle.dumps(deferred_priority_email), priority=Email.Priorities.DEFERRED)

    assert Email.objects.count() == 6
    assert EmailLog.objects.count() == 0

    settings.EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    send_emails()

    assert Email.objects.count() == 1
    assert EmailLog.objects.count() == 5

    sent_emails = [log.email for log in EmailLog.objects.all().order_by("id")]
    assert sent_emails[0].subject == "High Priority"
    assert sent_emails[1].subject == "Medium Priority"
    assert sent_emails[3].subject == "Low Priority"

    assert mock_send_messages.call_count == 5


@pytest.mark.django_db
@patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
def test_send_emails_no_emails(mock_send_messages: MagicMock) -> None:
    mock_send_messages.return_value = 1

    assert Email.objects.count() == 0
    assert EmailLog.objects.count() == 0

    send_emails()

    assert Email.objects.count() == 0
    assert EmailLog.objects.count() == 0


@pytest.mark.django_db
@patch("django_nitro_mailer.tasks.get_connection")
@patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
def test_send_emails_backend_error(mock_send_messages: MagicMock, mock_get_connection: MagicMock) -> None:
    mock_send_messages.side_effect = Exception("Backend error")

    mock_backend = MagicMock()
    mock_get_connection.return_value = mock_backend
    mock_backend.send_messages = mock_send_messages

    email_message = EmailMessage(
        subject="Test Subject", body="Test Body", from_email="from@example.com", to=["to@example.com"]
    )
    Email.objects.create(email_data=pickle.dumps(email_message), priority=Email.Priorities.HIGH)

    assert Email.objects.count() == 1
    assert EmailLog.objects.count() == 0

    send_emails()

    assert Email.objects.count() == 1
    assert EmailLog.objects.count() == 1
    email_log = EmailLog.objects.first()
    assert email_log.result == EmailLog.Results.FAILURE
    assert email_log.email_data == pickle.dumps(email_message)


@pytest.mark.django_db
@patch("django.core.mail.backends.base.BaseEmailBackend.send_messages")
@patch("django.core.mail.backends.console.EmailBackend")
def test_send_mass_email_success(mock_send_mass_mail: MagicMock, mock_get_connection: MagicMock) -> None:
    mock_send_mass_mail.return_value = 3

    settings.EMAIL_BACKEND = "django_nitro_mailer.backend.DatabaseBackend"
    settings.NITRO_MAILER_EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    message1 = ("Subject 1", "Message 1", "from@example.com", ["to1@example.com", "to2@example.com", "to3@example.com"])
    message2 = ("Subject 2", "Message 2", "from@example.com", ["to2@example.com"])
    message3 = ("Subject 3", "Message 3", "from@example.com", ["to3@example.com"])

    send_mass_mail((message1, message2, message3), fail_silently=False)

    assert Email.objects.count() == 3
    assert EmailLog.objects.count() == 0

    send_emails(Email.objects.all())

    assert EmailLog.objects.count() == 3

    email_logs = EmailLog.objects.all()
    for email_log in email_logs:
        assert email_log.result == EmailLog.Results.SUCCESS


@pytest.mark.django_db
@patch("smtplib.SMTP")
def test_sync_backend_sends_email(mock_send_messages: MagicMock) -> None:
    settings.EMAIL_BACKEND = "django_nitro_mailer.backend.SyncBackend"
    settings.NITRO_MAILER_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    backend = SyncBackend()
    email_message = EmailMessage(
        subject="Test Subject",
        body="This is a test message.",
        from_email="from@example.com",
        to=["to@example.com"],
    )
    print(email_message)

    mock_send_messages.return_value.sendmail.return_value = None
    sent_count = backend.send_messages([email_message])

    assert sent_count == 1


@pytest.mark.django_db
@patch("smtplib.SMTP")
def test_sync_backend_sends_email_failure(mock_smtp: MagicMock) -> None:
    settings.EMAIL_BACKEND = "django_nitro_mailer.backend.SyncBackend"
    settings.NITRO_MAILER_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    backend = SyncBackend()
    email_message = EmailMessage(
        subject="Test Subject",
        body="This is a test message.",
        from_email="from@example.com",
        to=["to@example.com"],
    )

    mock_smtp.return_value.sendmail.side_effect = Exception("Failed to send email")

    sent_count = backend.send_messages([email_message])

    assert sent_count == 0
    mock_smtp.return_value.sendmail.assert_called_once()
