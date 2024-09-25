# Email Sending Guide

This documentation covers how to send emails using the two available backends, `SyncBackend` and `DatabaseBackend`, as well as how to configure throttling and logging features.

## Available Backends

### SyncBackend

The `SyncBackend` is designed for synchronous email sending. When using this backend, emails are sent immediately, and the application waits for a response from the email server to confirm whether the email was successfully delivered or failed.

#### How to Use `SyncBackend`


#### Step 1: Configure in Settings: 
Make sure to add the SyncBackend in your Django settings. You can set it as your email backend like this:

    # settings.py
    EMAIL_BACKEND = "django_nitro_mailer.backend.SyncBackend"
    NITRO_MAILER_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # or any other backend you prefer


#### Step 2: Sending Emails: 
To send emails using the `SyncBackend`, you can use the `send_mail` function directly. Here's an example:

    from django.core.mail import send_mail
    # Sending an email
    send_mail(
        subject="Welcome!",
        message="Hello, this is your welcome email.",
        from_email="admin@example.com",
        recipient_list=["user@example.com"],
        fail_silently=False,
    )

With this setup, the SyncBackend will manage the synchronous sending of your emails, confirming whether each email was successfully delivered or if there were any issues.

### DatabaseBackend

The DatabaseBackend is designed for *asynchronous email sending*. Emails are first stored in the database, allowing them to be processed later. This is useful when you want to queue emails for batch processing or need to manage a large volume of emails.
With this backend, emails are not sent immediately. Instead, they are saved in the Email model, and a separate process handles the actual sending. This decoupling helps ensure that email sending does not block other application processes, especially in high-traffic situations.

#### How to Use `DatabaseBackend`

To use `DatabaseBackend`, you configure it in Django settings, send emails as usual, and then trigger the task to process the queued emails.

#### Step 1: Configure the Backend

In your Django settings, set the email backend to DatabaseBackend:

    # settings.py
    EMAIL_BACKEND = "django_nitro_mailer.backend.DatabaseBackend"
    NITRO_MAILER_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # or any other backend you prefer

In this configuration, `DatabaseBackend` stores the emails in the database, and NITRO_MAILER_EMAIL_BACKEND defines the actual backend used to send the emails (in this case, the SMTP backend).

#### Step 2: Sending Emails: 
To send emails using the `DatabaseBackend`, you can use the `send_mail` function directly. Here's an example:

    from django.core.mail import send_mail
    # Sending an email
    send_mail(
        subject="Welcome!",
        message="Hello, this is your welcome email.",
        from_email="admin@example.com",
        recipient_list=["user@example.com"],
        fail_silently=False,
    )

With this setup, the SyncBackend will manage the synchronous sending of your emails, confirming whether each email was successfully delivered or if there were any issues.
