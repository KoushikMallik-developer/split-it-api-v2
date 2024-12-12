# Generated by Django 5.1.3 on 2024-12-12 18:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("username", models.CharField(max_length=25)),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="Email"
                    ),
                ),
                ("fname", models.CharField(max_length=255)),
                ("lname", models.CharField(max_length=255)),
                ("password", models.CharField(max_length=255)),
                ("dob", models.DateField(null=True)),
                ("phone", models.CharField(max_length=15, null=True)),
                ("image", models.CharField(max_length=2555, null=True)),
                ("is_active", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
