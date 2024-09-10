import pickle
from typing import Self

from django.core.mail import EmailMessage
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class EmailDataMixin(models.Model):
    email_data = models.BinaryField()

    class Meta:
        abstract = True
        app_label = 'django_nitro_mailer'

    def set_email(self: Self, email: EmailMessage) -> None:
        self.email_data = pickle.dumps(email)

    @cached_property
    def email(self: Self) -> EmailMessage | None:
        if self.email_data is not None:
            return pickle.loads(self.email_data)  # noqa: S301
        else:
            return None

    @cached_property
    def recipients(self: Self) -> list[str]:
        email = self.email
        if email is not None:
            return email.to
        else:
            return []

    @cached_property
    def subject(self: Self) -> str:
        email = self.email
        if email is not None:
            return email.subject
        else:
            return ""


class Email(EmailDataMixin, models.Model):
    class Priorities(models.IntegerChoices):
        DEFERRED = 0, _("Deferred")
        LOW = 10, _("Low")
        MEDIUM = 20, _("Medium")
        HIGH = 30, _("High")

    DEFAULT_PRIORITY = Priorities.MEDIUM

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    priority = models.PositiveSmallIntegerField(
        choices=Priorities.choices,
        default=DEFAULT_PRIORITY,
        help_text=_("Determines the order in which emails are sent."),
    )

    def __str__(self: Self) -> str:
        return f"{self.subject} [{self.created_at}]"


class EmailLog(EmailDataMixin, models.Model):
    class Results(models.IntegerChoices):
        SUCCESS = 0, _("Success")
        FAILURE = 1, _("Failure")

    result = models.PositiveSmallIntegerField(choices=Results.choices)

    def __str__(self: Self) -> str:
        return f"{self.result}: {self.subject} [{self.created_at}]"
