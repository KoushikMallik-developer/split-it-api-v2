# Generated by Django 5.1.3 on 2024-12-13 19:43

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth_api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserEmailVerification",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=6)),
                ("expiration_time", models.DateTimeField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="auth_api.user"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
