# Generated by Django 5.0.3 on 2024-04-04 07:36

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("category", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "transaction_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=256)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[("expense", "expense"), ("income", "income")],
                        default="expense",
                        max_length=8,
                    ),
                ),
                ("transaction_time", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transaction_category",
                        to="category.category",
                    ),
                ),
            ],
        ),
    ]
