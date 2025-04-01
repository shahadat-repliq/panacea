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


class ProductForm(models.TextChoices):
    TABLETS = "TABLETS", "Tablets"
    SYRUP = "SYRUP", "Syrup"
    INJECTION = "INJECTION", "Injection"
    OINTMENT = "OINTMENT", "Ointment"
    CAPSULE = "CAPSULE", "Capsule"
    DEFAULT = "NONE", "None"
