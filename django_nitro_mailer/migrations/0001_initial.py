# Generated by Django 4.2.13 on 2024-05-19 18:35

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Email",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email_data", models.BinaryField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "priority",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Deferred"), (10, "Low"), (20, "Medium"), (30, "High")], default=20
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EmailLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email_data", models.BinaryField()),
                ("result", models.PositiveSmallIntegerField(choices=[(0, "Success"), (1, "Failure")])),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
