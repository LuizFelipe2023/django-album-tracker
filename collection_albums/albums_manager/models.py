from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo e-mail é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('e-mail', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100, blank=True, null=True)
    formed_year = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='albums')
    release_year = models.PositiveIntegerField()
    cover_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.artist.name} ({self.release_year})"


class CollectionItem(models.Model):
    FORMAT_CHOICES = [
        ('VINYL_12', 'Vinil 12" (LP)'),
        ('VINYL_7', 'Vinil 7" (Compacto)'),
        ('CD', 'CD'),
        ('CASSETTE', 'Fita K7'),
        ('DIGITAL', 'Digital / Streaming'),
    ]

    CONDITION_CHOICES = [
        ('M', 'Mint (Perfeito, lacrado)'),
        ('NM', 'Near Mint (Como novo)'),
        ('VG', 'Very Good (Marcas leves de uso)'),
        ('G', 'Good (Desgastado)'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collection_items'
    )
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='collection_entries')
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='VINYL_12')
    condition = models.CharField(max_length=5, choices=CONDITION_CHOICES, default='NM')
    notes = models.TextField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.album.title} ({self.get_format_display()})"
