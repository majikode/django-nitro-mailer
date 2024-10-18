#!/usr/bin/env python

"""
manage.py script used by django-nitro-mailer developers to create
DB migrations, test management commands and serve the admin page.
"""

import os

if __name__ == "__main__":
    from django.core import management

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dev_settings")
    management.execute_from_command_line()
