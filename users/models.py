import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el email, nombre, apellido y contraseña dados.
        """
        if not email:
            raise ValueError(_('El correo electrónico es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con el email, nombre, apellido y contraseña dados.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('El superusuario debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('El superusuario debe tener is_superuser=True.'))

        return self.create_user(email, first_name, last_name, password, **extra_fields)


# Usuario con roles específicos
class User(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('INVESTIGADOR', 'Investigador'),
        ('OPERADOR', 'Operador de Recolección'),
    )
    rol = models.CharField(max_length=15, choices=ROLES, default='INVESTIGADOR',
                           help_text="Rol del usuario en el sistema")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.username} ({self.rol})"

    objects = CustomUserManager()

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({
                'email': _('Ya existe una cuenta con este correo electrónico.')
            })

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_unique_username()
        super().save(*args, **kwargs)

    def generate_unique_username(self):
        return str(uuid.uuid4())[:16]

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')