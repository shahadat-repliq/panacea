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


class DeliveryStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    ON_THE_WAY = "ON_THE_WAY", "On The Way"
    COMPLETED = "COMPLETED", "Completed"
    CANCELED = "CANCELED", "Canceled"


class ProductRequestStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    CANCELED = "CANCELED", "Canceled"
