from typing import Self

from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import URLPattern, path

from django_nitro_mailer.emails import send_emails
from django_nitro_mailer.forms import EmailAdminForm
from django_nitro_mailer.models import Email


@admin.action(description="Send selected emails")
def send_selected_emails(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    result = send_emails(queryset)
    msg = f"Successfully sent {result.success_count} email(s)."
    if result.failure_count > 0:
        msg += f" Failed to send {result.failure_count} email(s)."
        messages.warning(request, msg)
    else:
        messages.success(request, msg)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    change_form_template = "admin/email_change_form.html"

    form = EmailAdminForm
    list_display = ("subject", "recipients", "created_at", "priority")
    actions = (send_selected_emails,)

    def get_urls(self: Self) -> list[URLPattern]:
        urls = super().get_urls()
        custom_urls = [
            path(
                "send-email/<int:email_id>/",
                self.admin_site.admin_view(self.send_email),
                name="send_email",
            ),
        ]
        return custom_urls + urls

    def send_email(self: Self, request: HttpRequest, email_id: int) -> HttpResponse:
        email = Email.objects.filter(id=email_id)
        result = send_emails(queryset=email)
        if result.success_count > 0:
            messages.success(request, "Email sent successfully.")
        else:
            messages.error(request, "Failed to send email.")
        
        app_label = self.opts.app_label
        model_name = self.opts.model_name
        return redirect(f"admin:{app_label}_{model_name}_changelist")
