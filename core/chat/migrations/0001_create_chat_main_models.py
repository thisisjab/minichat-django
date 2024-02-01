# Generated by Django 5.0.1 on 2024-01-31 20:05

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.UUID("1863172a-be93-41b7-8069-ca2836c7cf63"),
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("P", "Private Chat"), ("G", "Group Chat")],
                        editable=False,
                        max_length=1,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Participation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is active"),
                ),
                (
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participations",
                        to="chat.chat",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="chat",
            name="participants",
            field=models.ManyToManyField(
                related_name="chats",
                through="chat.Participation",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Participants",
            ),
        ),
        migrations.CreateModel(
            name="TextMessage",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(auto_now=True, verbose_name="Modified at"),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.UUID("2ecd3acc-f492-4d1d-8bde-f9fa0dad8f35"),
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.CharField(max_length=255, verbose_name="Body")),
                (
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="chat.chat",
                        verbose_name="Chat",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]