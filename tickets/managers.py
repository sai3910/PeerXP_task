from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Q

class UserQuerySet(models.query.QuerySet):
    def get_user(self, value):
        return self.filter(
            Q(email__iexact=value) |
            Q(mobile=value)
        )

    def get_by_id(self, value):
        return self.filter(
            Q(id=value)
        )

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True
    def get_user(self, value):
        """
        get user object by id or email or mobile number.
        """
        if isinstance(value, int):
            user_qs = self.get_queryset().get_by_id(value)
            return user_qs
        user_qs = self.get_queryset().get_user(value)
        return user_qs

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
