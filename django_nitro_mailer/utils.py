from django.core.mail import EmailMultiAlternatives


def create_email_message(
    subject: str,
    recipients: list[str],
    text_content: str,
    html_content: str | None = None,
    from_email: str | None = None,
    attachments: list[str] | None = None,
) -> EmailMultiAlternatives:
    email = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=from_email, to=recipients, attachments=attachments
    )
    if html_content:
        email.attach_alternative(html_content, "text/html")

    return email
