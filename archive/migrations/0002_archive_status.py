# Generated by Django 4.2.1 on 2023-05-06 16:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("archive", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="archive",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "pending"),
                    ("enqueued", "enqueued"),
                    ("complete", "complete"),
                    ("failed", "failed"),
                ],
                db_index=True,
                default="pending",
                max_length=255,
            ),
        ),
    ]
