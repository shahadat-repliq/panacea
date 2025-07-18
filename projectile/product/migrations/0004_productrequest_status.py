# Generated by Django 5.1.6 on 2025-04-14 17:27

import shared.choices
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0003_productrequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="productrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "Pending"),
                    ("APPROVED", "Approved"),
                    ("REJECTED", "Rejected"),
                    ("CANCELED", "Canceled"),
                ],
                default="PENDING",
                verbose_name=shared.choices.ProductRequestStatus,
            ),
        ),
    ]
