# Generated by Django 5.1.6 on 2025-03-11 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="last_login",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last login"
            ),
        ),
    ]
