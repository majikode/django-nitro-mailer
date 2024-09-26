from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path

from django_nitro_mailer.emails import send_emails
from django_nitro_mailer.forms import EmailAdminForm
from django_nitro_mailer.models import Email


@admin.action(description="Send selected emails")
def send_selected_emails(modeladmin, request, queryset):
    try:
        count = queryset.count()
        send_emails(queryset)
        messages.success(request, "Successfully sent %s email(s)." % count)
    except Exception as e:
        messages.error(request, "An error occurred while sending emails: %s" % e)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    change_form_template = "admin/email_change_form.html"

    form = EmailAdminForm
    list_display = ("subject", "recipients", "created_at", "priority")
    actions = [send_selected_emails]

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
