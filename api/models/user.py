from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.utils.text import slugify
import random
from datetime import timedelta

# Create your models here.

# Users roles
NONE = 0
REGULAR_USER = 1
COUNSELOR = 2
MODERATOR = 3

ROLES = [
    (NONE, 'NONE'),
    (REGULAR_USER, 'USER'),
    (COUNSELOR, 'COUNSELOR'),
    (MODERATOR, 'MODERATOR'),
]


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_unique_id(self):
        allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        unique_id = get_random_string(length=6, allowed_chars=allowed_chars)
        while self.__class__.objects.filter(id=unique_id).exists():
            unique_id = get_random_string(
                length=6, allowed_chars=allowed_chars)
        return unique_id

    def generate_unique_slug(self, data="N/A"):
        num = 1
        new_slug = slugify(data=data)
        while self.__class__.objects.filter(slug=new_slug).exists():
            new_slug = f"{new_slug}-{num}"
            num += 1
        return new_slug

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    id = models.CharField(primary_key=True, max_length=6, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=250, default='N/A')
    is_active = models.BooleanField(default=True)
    email_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role = models.IntegerField(choices=ROLES, default=NONE)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry_date = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()

        user = self.__class__.objects.filter(id=self.id).first()
        if not user or user and user.password != self.password:
            self.set_password(self.password)

        if user and not user.is_superuser and self.is_superuser:
            self.is_staff = True

        super().save(*args, **kwargs)

    def generate_otp(self, length=6, hours=24):
        characters = '0123456789'
        if not self.otp_expiry_date or not self.otp or timezone.now() > self.otp_expiry_date:
            otp = ''.join(random.choice(characters) for _ in range(length))
            self.otp = otp
            self.otp_expiry_date = timezone.now() + timedelta(hours=hours)
            self.save()
        return self.otp

    def verify_otp(self, otp, verify_and_clear=True):
        origin_otp = self.otp
        origin_otp_expiry_date = self.otp_expiry_date

        if not otp or not origin_otp or not origin_otp_expiry_date:
            return False

        if verify_and_clear:
            self.otp = None
            self.otp_expiry_date = None
            self.save()

        return timezone.now() < origin_otp_expiry_date and origin_otp == otp

    @property
    def is_none(self):
        return self.role == NONE

    @property
    def is_regular_user(self):
        return self.role == REGULAR_USER

    @property
    def is_counselor(self):
        return self.role == COUNSELOR

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return f'{self.email} {self.username}'


class RegularUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profession = models.CharField(max_length=250, default='N/A')

    def save(self, *args, **kwargs):
        user = User.objects.filter(id=self.user.id).first()
        if user and not user.is_regular_user:
            user.role = REGULAR_USER
            user.save()

        super().save(*args, **kwargs)


class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    qualification = models.CharField(max_length=250, default='N/A')
    description = models.CharField(max_length=250, default='N/A')

    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        user = User.objects.filter(id=self.user.id).first()
        if user and not user.is_counselor:
            user.role = COUNSELOR
            user.save()

        super().save(*args, **kwargs)


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    qualification = models.CharField(max_length=250, default='N/A')

    def save(self, *args, **kwargs):
        user = User.objects.filter(id=self.user.id).first()
        if user and not user.is_moderator:
            user.role = MODERATOR
            user.save()

        super().save(*args, **kwargs)
