from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator


class BaseUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telefono = models.IntegerField(
        validators=[MinValueValidator(111111111), MaxValueValidator(999999999)]
    )
    direccion = models.CharField(max_length=50)
    imagen_perfil = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.get_username()


class Persona(BaseUser):
    nombre = models.CharField("Nombre", max_length=50)
    apellido = models.CharField("Apellido", max_length=50)
    fec_nac = models.DateField(blank=True, null=True)
    documento = models.URLField(max_length=200, blank=True, null=True)

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


# Define la función genérica para establecer is_active en False para el usuario asociado
def set_user_inactive(sender, instance, created, **kwargs):
    if created:
        # Establece is_active en False para el usuario asociado
        instance.user.is_active = False
        instance.user.save()


# Registra la señal para los modelos Persona, Organizacion y Administrador
@receiver(post_save, sender=Persona)
@receiver(post_save, sender=Organizacion)
def handle_user_creation(sender, instance, created, **kwargs):
    set_user_inactive(sender, instance, created, **kwargs)


@receiver(post_delete, sender=Persona)
@receiver(post_delete, sender=Organizacion)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()
