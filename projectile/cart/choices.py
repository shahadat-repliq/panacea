from django.db.models import TextChoices


class CartActionchoices(TextChoices):
    DELETE = "DELETE", "Delete"
    ADD = "ADD", "Add"
