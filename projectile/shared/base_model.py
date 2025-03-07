import uuid

from django.db import models
from .choices import StatusChoices


class BaseUserModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=StatusChoices.choices, default=StatusChoices.ACTIVE
    )

    class Meta:
        abstract = True

    def get_active_instance(self):
        return self.__class__.objects.filter(status=StatusChoices.ACTIVE)


class BaseProductModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
