# `django-nitro-mailer`

`django-nitro-mailer` is a pluggable Django app that provides extra email reliability and observability in form of email backends that can be used with Django's built-in functions and other email backend.

`django-nitro-mailer` by itself does not provide a way to send emails, but it puts an extra layer before the email backend to provide extra features like:

* priority queueing
* retrying failed emails
* logging and traces
* email throttling
* sending messages through the admin panel

