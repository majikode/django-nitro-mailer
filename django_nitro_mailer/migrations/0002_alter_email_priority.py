# Generated by Django 4.2 on 2024-09-04 09:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_nitro_mailer", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="email",
            name="priority",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "Deferred"), (10, "Low"), (20, "Medium"), (30, "High")],
                default=20,
                help_text="Determines the order in which emails are sent.",
            ),
        ),
    ]
