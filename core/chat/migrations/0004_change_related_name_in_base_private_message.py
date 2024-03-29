# Generated by Django 5.0.1 on 2024-02-06 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0003_convert_participants_to_many_2_many_field"),
    ]

    operations = [
        migrations.AlterField(
            model_name="privatetextmessage",
            name="related_chat",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to="chat.privatechat",
                verbose_name="Related chat",
            ),
        ),
    ]
