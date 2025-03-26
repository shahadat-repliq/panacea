from django.db import models


class StatusChoices(models.TextChoices):
    ACTIVE = (
        "ACTIVE",
        "Active",
    )
    INACTIVE = "INACTIVE", "Inactive"
    PENDING = "PENDING", "Pending"
    DELETED = "DELETED", "Deleted"


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    OWNER = "OWNER", "Owner"
    MANAGER = "MANAGER", "Manager"
    STAFF = "STAFF", "Staff"
    CUSTOMER = "CUSTOMER", "Customer"
