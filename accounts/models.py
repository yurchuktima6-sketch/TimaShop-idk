from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    gamer_tag = models.CharField(max_length=50, blank=True, null=True, verbose_name="Геймертаг")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Про себе")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    favorite_platform = models.CharField(max_length=50, blank=True, verbose_name="Улюблена платформа")

    def __str__(self):
        return f"Профіль {self.user.username}"