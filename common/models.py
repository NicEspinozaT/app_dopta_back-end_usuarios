from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Usuario(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    @property
    def is_persona(self):
        return hasattr(self, "persona")

    @property
    def is_organizacion(self):
        return hasattr(self, "organizacion")

    @property
    def is_administrador(self):
        return hasattr(self, "administrador")
