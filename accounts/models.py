from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Egyptian mobile: 010 / 011 / 012 / 015 + 8 digits (req 5)
egyptian_phone = RegexValidator(
    regex=r'^01[0125][0-9]{8}$',
    message='Enter a valid Egyptian mobile number (e.g. 01012345678).',
)


class CustomUser(AbstractUser):
    """Req 2,3: email unique + first/last name + mobile phone. Login with email (req 6)."""
    username = None  # we login with email, not username
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, validators=[egyptian_phone])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email
