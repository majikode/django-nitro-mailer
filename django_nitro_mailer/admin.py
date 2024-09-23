from django.contrib import admin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import path
from django.utils.html import format_html
from django.urls import reverse
from django_nitro_mailer.forms import EmailAdminForm
from django_nitro_mailer.models import Email
from django_nitro_mailer.tasks import send_emails


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    form = EmailAdminForm

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "send-email/<int:email_id>/",
                self.admin_site.admin_view(self.send_email),
                name="send_email",
            ),
        ]
        return custom_urls + urls

    def send_email(self, request, email_id):
        try:
            email = Email.objects.filter(id=email_id)
            send_emails(queryset=email)
            messages.success(request, "Email has been sent.")
        except Exception as e:
            messages.error(request, f"Error while sending email: {e}")
        return redirect(request.META.get("HTTP_REFERER", "admin:index"))

    def email_action_button(self, obj):
        url = reverse("admin:send_email", args=[obj.pk])
        return format_html('<a class="button" href="{}">Send email</a>', url)

    list_display = ("subject", "recipients", "created_at", "priority", "email_action_button")
