from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom manager for creating users of type CustomUser."""

    def create_user(self, full_name, email, password, **extra_fields):
        """
        Create user account.
        Args:
            full_name: user name
            email: user email
            password: user password
            **extra_fields: additional user fields such as user role

        Returns: created user of type CustomUser
        """
        if not full_name:
            raise ValueError(_("The full name must be set"))
        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        if not extra_fields.get('role'):
            raise ValueError('User must have a role')

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, full_name, email, password, **extra_fields):
        """
        Create superuser account.
        Args:
            full_name: superuser name
            email: superuser email
            password: superuser password
            **extra_fields: additional superuser fields such as user role

        Returns: created superuser of type CustomUser
        """
        from accounts.models import UserRoles

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', UserRoles.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') != UserRoles.ADMIN:
            raise ValueError('Superuser must have role of Global Admin')
        return self.create_user(full_name, email, password, **extra_fields)
