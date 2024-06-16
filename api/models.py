from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from firebasestorage.firebase import bucket

DV_choices = {
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "K": "k",
}


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
    fec_nac = models.DateField()
    documento = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"


class Organizacion(BaseUser):
    numrut_org = models.IntegerField(
        validators=[MinValueValidator(1111111), MaxValueValidator(99999999)]
    )
    dv = models.CharField('Digito verificador',choices=DV_choices)
    razon_social = models.CharField("Razon social", max_length=50)
    telefono2 = models.IntegerField(
        validators=[MinValueValidator(111111111), MaxValueValidator(999999999)]
    )

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
def create_persona_profile(sender, instance, created, **kwargs):
    if created:
        instance.user.is_persona = True
        instance.user.save()
        set_user_inactive(sender, instance, created, **kwargs)


@receiver(post_save, sender=Organizacion)
def create_organizacion_profile(sender, instance, created, **kwargs):
    if created:
        instance.user.is_organizacion = True
        instance.user.save()
        set_user_inactive(sender, instance, created, **kwargs)


@receiver(post_delete, sender=Persona)
@receiver(post_delete, sender=Organizacion)
def eliminar_usuario(sender, instance, **kwargs):
    if instance.imagen_perfil:
        blob_name = instance.imagen_perfil.split("/")[-1]
        blob = bucket.blob(f"imagen_perfil/{blob_name}")
        blob.delete()

    if hasattr(instance, "documento") and instance.documento:
        doc_name = instance.documento.split("/")[-1]
        blob = bucket.blob(f"doc_user/{instance.user.username}/{doc_name}")
        blob.delete()
    instance.user.delete()
