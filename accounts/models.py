import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser, Group
from django.core.validators import validate_email
from django.db import models
from django.db.models import CASCADE
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model with roles and email address is the unique identifier."""
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, validators=[validate_email])
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    modified_date = models.DateTimeField(default=timezone.now, editable=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, editable=False)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{_("Name")}: {_(self.full_name)} | {_("Email")}: {self.email}'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class UserProfile(models.Model):
    """Basic model for user profiles."""
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    user = models.OneToOneField(CustomUser, on_delete=CASCADE)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    modified_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        abstract = True


class InstructorProfile(UserProfile):
    """Model for instructor profiles."""
    class Meta:
        verbose_name = _('instructor')
        verbose_name_plural = _('instructors')


class StudentProfile(UserProfile):
    """Model for student profiles."""
    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')

