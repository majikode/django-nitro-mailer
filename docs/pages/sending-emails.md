# Email Sending

This documentation covers how to send emails using the available email backends.

## Available Backends

### `DatabaseBackend`

The `DatabaseBackend` is designed for *asynchronous email sending*. Emails are first stored in the database, allowing them to be processed later. 

This allows for reliable email delivery (because the emails are stored until successfully sent), batch processing, and potentially better performance by decoupling the email sending process from the application.

#### Usage

To use `DatabaseBackend`, you need to configure it as your main email backend, create emails entries either directly or using Django's built-in functions, and then trigger the sending of queued emails.

#### Step 1: Configuring the Backend

In your Django settings, set the email backend to `DatabaseBackend`:

```python
# settings.py
EMAIL_BACKEND = "django_nitro_mailer.backend.DatabaseBackend"
NITRO_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # or your preferred email backend
```

In this configuration, `DatabaseBackend` stores the emails in the database, and `NITRO_EMAIL_BACKEND` defines the actual backend used to send the emails (in this case, the SMTP backend).

#### Step 2: Creating email entries
To send emails using the `DatabaseBackend`, you can use the `send_mail` function directly. Here's an example:

```python
from django.core.mail import send_mail

send_mail(
    subject="Welcome!",
    message="Hello, this is your welcome email.",
    from_email="admin@example.com",
    recipient_list=["user@example.com"],
    fail_silently=False,
)
```

Or you can create an `Email` object directly from an `EmailMessage`. This has the advantage that you can specify the email's priority.

```python
from django.core.mail import EmailMessage

from django_nitro_mailer.models import Email

email_message = EmailMessage(
    subject="Welcome!",
    body="Hello, this is your welcome email.",
    from_email="admin@example.com",
    to=["user@example.com"],
)
email = Email(priority=Email.Priorities.HIGH)
email.set_email(email_message)
email.save()
```


### Step 3: Sending emails

Once you've configured the `DatabaseBackend` and created you email entries, at any given time you can use the following options to send the queued emails:

#### Call the `send_emails` function

You can import and call the `send_emails` function to send all queued emails:

```python
from django_nitro_mailer.emails import send_emails

send_emails()
```

#### Django Admin

The Django admin interface provides a way to send emails manually. You can select the emails you want to send and use the "Send selected emails" action from the dropdown.

#### Management command

A management command is provided which makes it easy to with crontab:

```bash
$ python manage.py send_emails
```

### SyncBackend

The `SyncBackend` is designed for synchronous email sending. When using this backend, emails are sent immediately, and the application waits for a response from the email server to confirm whether the email was successfully delivered or failed, creating log entries for each email sent.

#### Usage

To use the `SyncBackend`, you need to configure it as your main email backend and then send emails using Django's built-in functions.

```python
# settings.py
EMAIL_BACKEND = "django_nitro_mailer.backend.SyncBackend"
NITRO_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # or your preferred email backend
```

Use the built-in function to send emails:

```python
from django.core.mail import send_mail

send_mail(
    subject="Welcome!",
    message="Hello, this is your welcome email.",
    from_email="admin@example.com",
    recipient_list=["user@example.com"],
    fail_silently=False,
)
```

