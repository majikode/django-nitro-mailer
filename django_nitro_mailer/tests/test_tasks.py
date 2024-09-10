import pytest
import pickle
from unittest.mock import patch, MagicMock
from django.conf import settings
from django.core.mail import EmailMessage
from django_nitro_mailer.tasks import send_emails
from django_nitro_mailer.models import Email, EmailLog
from unittest.mock import patch


@pytest.mark.django_db
def test_set_and_get_email():
    email_instance = Email.objects.create(email_data=b"")

    email_message = EmailMessage(
        subject="Test Subject", body="Test Body", from_email="from@example.com", to=["to@example.com"]
    )

    email_instance.set_email(email_message)

    assert email_instance.email.subject == "Test Subject"
    assert email_instance.email.body == "Test Body"
    assert email_instance.recipients == ["to@example.com"]


@pytest.mark.django_db
def test_email_model():

    email_instance = Email.objects.create(priority=Email.Priorities.HIGH, email_data=b"")
    assert email_instance.priority == Email.Priorities.HIGH


@pytest.mark.django_db
@patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
def test_send_emails_success_smtp(mock_send_messages):
    mock_send_messages.return_value = 1

    email_message = EmailMessage(
        subject="Test Subject", body="Test Body", from_email="from@example.com", to=["to@example.com"]
    )

    email = Email.objects.create(email_data=pickle.dumps(email_message), priority=Email.Priorities.HIGH)

    assert Email.objects.count() == 1
    assert EmailLog.objects.count() == 0

    from django.conf import settings

    settings.EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    send_emails()

    assert Email.objects.count() == 0
    assert EmailLog.objects.count() == 1

    email_log = EmailLog.objects.first()
    assert email_log.result == EmailLog.Results.SUCCESS
    assert email_log.email_data == pickle.dumps(email_message)

    mock_send_messages.assert_called_once()


@pytest.mark.django_db
def test_send_emails_success_console():
    email_message = EmailMessage(
        subject="Test Subject", body="Test Body", from_email="from@example.com", to=["to@example.com"]
    )

    email = Email.objects.create(email_data=pickle.dumps(email_message), priority=Email.Priorities.HIGH)

    assert Email.objects.count() == 1
    assert EmailLog.objects.count() == 0

    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    send_emails()

    assert Email.objects.count() == 0
    assert EmailLog.objects.count() == 1

    email_log = EmailLog.objects.first()
    assert email_log.result == EmailLog.Results.SUCCESS
    assert email_log.email_data == pickle.dumps(email_message)


@pytest.mark.django_db
@patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
def test_send_emails_with_priorities(mock_send_messages):
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

    Email.objects.create(email_data=pickle.dumps(high_priority_email), priority=Email.Priorities.HIGH)
    Email.objects.create(email_data=pickle.dumps(medium_priority_email), priority=Email.Priorities.MEDIUM)
    Email.objects.create(email_data=pickle.dumps(low_priority_email), priority=Email.Priorities.LOW)
    Email.objects.create(email_data=pickle.dumps(medium_priority_email_2), priority=Email.Priorities.MEDIUM)
    Email.objects.create(email_data=pickle.dumps(low_priority_email_2), priority=Email.Priorities.LOW)

    assert Email.objects.count() == 5
    assert EmailLog.objects.count() == 0

    settings.EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    send_emails()

    assert Email.objects.count() == 0
    assert EmailLog.objects.count() == 5

    sent_emails = [log.email for log in EmailLog.objects.all().order_by("id")]
    assert sent_emails[0].subject == "High Priority"
    assert sent_emails[1].subject == "Medium Priority"
    assert sent_emails[3].subject == "Low Priority"

    assert mock_send_messages.call_count == 5


@pytest.mark.django_db
@patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
def test_send_emails_no_emails(mock_send_messages):
    mock_send_messages.return_value = 1

    assert Email.objects.count() == 0
    assert EmailLog.objects.count() == 0

    send_emails()

    assert Email.objects.count() == 0
    assert EmailLog.objects.count() == 0


@pytest.mark.django_db
@patch("django_nitro_mailer.tasks.get_connection")
@patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
def test_send_emails_backend_error(mock_send_messages, mock_get_connection):
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
