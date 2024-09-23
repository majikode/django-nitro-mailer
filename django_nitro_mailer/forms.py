from typing import Any, Self

from django import forms
from django.template import Context, Template
from django.utils.translation import gettext_lazy

from django_nitro_mailer.array_field import SimpleArrayField
from django_nitro_mailer.utils import create_email_message


class EmailAdminForm(forms.ModelForm):
    recipients = SimpleArrayField(forms.EmailField(), widget=forms.TextInput(attrs={"class": "vTextField"}))
    subject = forms.CharField(widget=forms.TextInput(attrs={"class": "vTextField"}))
    text_content = forms.CharField(widget=forms.Textarea, required=False)
    html_content = forms.CharField(label=gettext_lazy("HTML content"), widget=forms.Textarea, required=False)
    context = forms.JSONField(
        required=False, initial={}, help_text=gettext_lazy("JSON context for rendering the email content.")
    )
    send_email = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())

    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        if instance := kwargs.get("instance", None):
            email = instance.email
            kwargs["initial"] = {
                "recipients": ",".join(email.to),
                "subject": email.subject,
                "text_content": email.body,
                "html_content": email.alternatives[0][0] if email.alternatives else "",
            }
        super().__init__(*args, **kwargs)

    def save(self: Self, commit: bool = True) -> Any:
        recipients = self.cleaned_data["recipients"]
        subject = self.cleaned_data["subject"]
        context = Context(self.cleaned_data["context"])
        text_content = Template(self.cleaned_data["text_content"]).render(context)
        html_content = Template(self.cleaned_data["html_content"]).render(context)
        kwargs = {
            "subject": subject,
            "recipients": recipients,
            "html_content": html_content,
            "text_content": text_content,
        }

        self.instance.set_email(create_email_message(**kwargs))

        return super().save(commit)
