import re
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def normalize_egyptian_phone(value):
    """010..., +20... or 0020... (spaces/dashes allowed) -> clean 01... number."""
    number = re.sub(r'[\s\-]', '', str(value))
    if number.startswith('+20'):
        number = '0' + number[3:]
    elif number.startswith('0020'):
        number = '0' + number[4:]
    return number


def validate_egyptian_phone(value):
    """Strict Egyptian mobile validation (req 5).

    Accepts 010/011/012/015 + 8 digits (with optional +20 country code)
    and rejects dummy numbers made of repeated or sequential digits.
    """
    number = normalize_egyptian_phone(value)
    if not re.fullmatch(r'01[0125][0-9]{8}', number):
        raise ValidationError(
            'Enter a valid Egyptian mobile number: 010, 011, 012 or 015 followed by 8 digits.')
    last8 = number[3:]
    if (len(set(last8)) == 1
            or last8 in '01234567890123456789'
            or last8 in '98765432109876543210'):
        raise ValidationError('This mobile number looks invalid. Please enter your real number.')


class CustomUserManager(BaseUserManager):
    """Manager that creates users with email instead of username."""
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Req 2,3: email unique + first/last name + mobile phone. Login with email (req 6)."""
    username = None  # we login with email, not username
    email = models.EmailField(unique=True)
    # max_length=16 so users can type +20 prefix / spaces; stored normalized (11).
    phone = models.CharField(max_length=16, validators=[validate_egyptian_phone])

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def save(self, *args, **kwargs):
        self.phone = normalize_egyptian_phone(self.phone)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
