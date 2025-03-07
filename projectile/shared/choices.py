from django.db.models import TextChoices


class StatusChoices(TextChoices):
    ACTIVE = (
        "ACTIVE",
        "Active",
    )
    INACTIVE = "INACTIVE", "Inactive"
    PENDING = "PENDING", "Pending"
    DELETED = "DELETED", "Deleted"
