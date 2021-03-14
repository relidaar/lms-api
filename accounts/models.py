import uuid

from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.db.models import TextChoices
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.managers import CustomUserManager


class UserRoles(TextChoices):
    """Represent user roles for CustomUser model."""
    STUDENT = 'ST', _('Student')
    INSTRUCTOR = 'IN', _('Instructor')
    ADMIN = 'AD', _('Admin')


class CustomUser(AbstractUser):
    """Custom user model with roles and email address is the unique identifier."""
    username = None
    first_name = None
    last_name = None

    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, validators=[validate_email])
    role = models.CharField(max_length=2, choices=UserRoles.choices)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{_("Name")}: {_(self.full_name)} | {_("Email")}: {self.email}'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
