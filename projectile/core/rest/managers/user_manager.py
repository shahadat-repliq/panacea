from phonenumbers import parse, is_valid_number
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(phone_number):
    try:
        parsed_number = parse(phone_number)

        if not is_valid_number(parsed_number):
            raise ValidationError(_("Invalid phone number."))
    except Exception as e:
        raise ValidationError(_("Invalid phone number format. Error: %s" % str(e)))


class UserManager(BaseUserManager):

    def create_user(
        self,
        phone_number,
        password=None,
        email=None,
        first_name=None,
        last_name=None,
        **extra_fields
    ):

        validate_phone_number(phone_number=phone_number)

        if email:
            self.normalize_email(email)

        user = self.model(
            phone_number=phone_number,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        phone_number,
        password,
        email=None,
        first_name=None,
        last_name=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValidationError(_("is_staff must be true for superusers."))
        if extra_fields.get("is_superuser") is not True:
            raise ValidationError(_("is_superuser must be true for superusers."))

        validate_phone_number(phone_number=phone_number)
        if email:
            self.normalize_email(email)
        user = self.create_user(
            phone_number=phone_number,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields,
        )
        return user
