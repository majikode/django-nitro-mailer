# to nie działa:

# from .tasks import send_emails, retry_deferred

# __all__ = ["send_emails", "retry_deferred"]


# to tez działa:

import django

django_initialized = False


def lazy_setup():
    global django_initialized
    if not django_initialized:
        django.setup()
        django_initialized = True


def send_emails(*args, **kwargs):
    lazy_setup()
    from .tasks import send_emails

    return send_emails(*args, **kwargs)


def retry_deferred(*args, **kwargs):
    lazy_setup()
    from .tasks import retry_deferred

    return retry_deferred(*args, **kwargs)


__all__ = ["send_emails", "retry_deferred"]
