# Generated by Django 5.0.1 on 2024-02-02 09:17

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0003_make_type_editable_for_chat_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chat",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("a696fb4f-3364-4d07-8cae-2d173a10137f"),
                editable=False,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="textmessage",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("27df61b0-ea11-49a2-bb96-536cd6929f61"),
                editable=False,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
    ]
