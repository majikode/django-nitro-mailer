from django.core.management.base import BaseCommand

from django_nitro_mailer.utils import send_emails


class Command(BaseCommand):
    help = "Send emails using the nitro email backend."

    def handle(self, *args, **kwargs):
        self.stdout.write("Sending emails")
        try:
            send_emails()
            self.stdout.write(self.style.SUCCESS("Emails sent successfully"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error sending emails: {e}"))
