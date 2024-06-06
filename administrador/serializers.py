from .models import Administrador
from rest_framework import serializers
from api.serializers import UserSerializer
from api.mixins import FirebaseImageMixin
from common.models import Usuario


# Administrador
class AdministradorSerializer(FirebaseImageMixin, serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Administrador
        fields = [
            "user",
            "telefono",
            "direccion",
            "admin_numrut",
            "admin_dv",
            "admin_p_nombre",
            "admin_s_nombre",
            "admin_apaterno",
            "admin_apmaterno",
            "admin_fec_nac",
            "imagen_perfil",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = Usuario.objects.create_superuser(**user_data)
        administrador = Administrador.objects.create(user=user, **validated_data)
        return administrador

    def update(self, instance, validated_data):
        imagen_perfil = validated_data.pop("imagen_perfil", None)
        if imagen_perfil:
            self.upload_image_to_firebase(instance, imagen_perfil)
        instance.telefono = validated_data.get("telefono", instance.telefono)
        instance.direccion = validated_data.get("direccion", instance.direccion)
        instance.admin_numrut = validated_data.get(
            "admin_numrut", instance.admin_numrut
        )
        instance.admin_dv = validated_data.get("admin_dv", instance.admin_dv)
        instance.admin_p_nombre = validated_data.get(
            "admin_p_nombre", instance.admin_p_nombre
        )
        instance.admin_s_nombre = validated_data.get(
            "admin_s_nombre", instance.admin_s_nombre
        )
        instance.admin_apaterno = validated_data.get(
            "admin_apaterno", instance.admin_apaterno
        )
        instance.admin_apmaterno = validated_data.get(
            "admin_apmaterno", instance.admin_apmaterno
        )
        instance.admin_fec_nac = validated_data.get(
            "admin_fec_nac", instance.admin_fec_nac
        )
        instance.save()

        return instance
