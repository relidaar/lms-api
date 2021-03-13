import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
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


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model with roles and email address is the unique identifier."""
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, validators=[validate_email])
    role = models.CharField(max_length=2, choices=UserRoles.choices)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{_("UID")}: {self.uid} | {_("Name")}:  {_(self.full_name)}'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        permissions = (
            ('create_admin', 'Create Admin'),
            ('create_instructor', 'Create Instructor'),
            ('create_student', 'Create Student'),
        )
