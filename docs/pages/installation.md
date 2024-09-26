# Installation Guide

This document will guide you through the installation process of the **django-nitro-mailer** .

## 1. Requirements

Before you begin, make sure your environment meets the following requirements:

- **Python 3.8+**
- **Django 3.2+**
- **PostgreSQL** or another database compatible with Django

If you use `poetry` or `pip`, ensure that you have an isolated environment set up, like a virtual environment or a containerized setup.

## 2. Installing the Package

To install the package, use the following steps:

### Using poetry
If you're managing dependencies with poetry, you can add it to your pyproject.toml file like this:

    poetry add django-nitro-mailer

## 3. Add the Application to Your Project
Once installed, add the application to your Django project's INSTALLED_APPS in settings.py:

    # settings.py

    INSTALLED_APPS = [
        # other apps
        'django_nitro_mailer',
    ]

## 4. Database Migrations
Run the migrations to create the necessary database tables for email logging:

    python manage.py migrate
    
This will ensure that the Email and EmailLog models are created in your database.


## 5. Configuration

### a. Environment Variables

Set up the necessary environment variables for the application to work correctly. Below are the key environment variables you need to configure:

- EMAIL_DB_LOGGING_ENABLED: Determines if emails should be logged in the database. Defaults to true.
- EMAIL_SEND_THROTTLE_MS: Sets a delay (in milliseconds) between sending each email, to avoid overloading your email server. Defaults to 0 (no delay).

Example .env file:

    EMAIL_DB_LOGGING_ENABLED=true
    EMAIL_SEND_THROTTLE_MS=1000

Make sure you load your environment variables in your Django settings file.

### b. Email Backend Configuration
Configure the email backend in settings.py. If using the custom email backends provided by this app (e.g., DatabaseBackend, SyncBackend), you can set it like this:

    # settings.py
    EMAIL_BACKEND = 'django_nitro_mailer.backends.DatabaseBackend'

Or for the synchronous email backend:

    EMAIL_BACKEND = 'django_nitro_mailer.backends.SyncBackend'

