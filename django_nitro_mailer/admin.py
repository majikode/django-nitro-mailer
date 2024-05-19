from django.contrib import admin

from django_nitro_mailer.forms import EmailAdminForm
from django_nitro_mailer.models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    form = EmailAdminForm

    list_display = ("subject", "recipients", "created_at", "priority")
