# Quickstart

This document will guide you through the installation process and initial setup of the `django-nitro-mailer` .

## Requirements

Before you begin, make sure your environment meets the following requirements:

- **Python 3.11+**
- **Django 4.2+**

## Installing the Package

Install the package using pip:

```bash
$ pip install django-nitro-mailer
```

## Usage

* Add `django_nitro_mailer` to your `INSTALLED_APPS` in your `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "django_nitro_mailer",
    ...
]
```

* Run `python manage.py migrate` to create the necessary tables.

* Change the `EMAIL_BACKEND` setting in your `settings.py` to use the desired backend:

**Database Backend**: Store emails in the database and send them asynchronously. Requires sending a cron job or some other scheduled task to send the emails.

```python
EMAIL_BACKEND = "django_nitro_mailer.backends.DatabaseBackend"
```

**Sync Backend**: Send emails synchronously. Does not provide the reliability that the database backend provides, but still provides the logging and throttling features.

```python
EMAIL_BACKEND = "django_nitro_mailer.backends.SyncBackend"
```
