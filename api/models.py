from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Usuario(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)


class BaseUser(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=50)
    imagen_perfil = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.get_username()


class Persona(BaseUser):
    nombre = models.CharField("Nombre", max_length=50)
    apellido = models.CharField("Apellido", max_length=50)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"


class Organizacion(BaseUser):
    rut_emp = models.IntegerField()
    razon_social = models.CharField("Razon social", max_length=50)
    telefono2 = models.IntegerField()

    class Meta:
        verbose_name = "Organizacion"
        verbose_name_plural = "Organizaciones"


class Administrador(BaseUser):
    admin_numrut = models.IntegerField("Numero de rut")
    admin_dv = models.CharField("Digito verificador", max_length=1)
    admin_p_nombre = models.CharField("Primer nombre", max_length=25)
    admin_s_nombre = models.CharField(
        "Segundo Nombre", max_length=25, blank=True, null=True
    )
    admin_apaterno = models.CharField("Apellido paterno", max_length=25)
    admin_apmaterno = models.CharField(
        "Apellido materno", max_length=25, blank=True, null=True
    )
    admin_fec_nac = models.DateField()

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"


# Define la función genérica para establecer is_active en False para el usuario asociado
def set_user_inactive(sender, instance, created, **kwargs):
    if created:
        # Establece is_active en False para el usuario asociado
        instance.user.is_active = False
        instance.user.save()


# Registra la señal para los modelos Persona, Organizacion y Administrador
@receiver(post_save, sender=Persona)
@receiver(post_save, sender=Organizacion)
@receiver(post_save, sender=Administrador)
def handle_user_creation(sender, instance, created, **kwargs):
    set_user_inactive(sender, instance, created, **kwargs)
