# Generated by Django 5.1.6 on 2025-03-31 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("organization", "0005_organizationproduct_is_custom_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="organizationproduct",
            name="status",
        ),
    ]
