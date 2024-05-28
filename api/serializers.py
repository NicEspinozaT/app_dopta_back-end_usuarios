from rest_framework import serializers
from .models import Persona, Organizacion, Administrador
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .mixins import FirebaseImageMixin

User = get_user_model()


# login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


# registro
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


# recuperar contraseña
class RecuPassRequestserializer(serializers.Serializer):
    email = serializers.EmailField()


class RecuPassConfirmserializer(serializers.Serializer):
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, data):
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data


# Persona
class PersonaSerializer(FirebaseImageMixin, serializers.ModelSerializer):
    user = UserSerializer()
    imagen_perfil = serializers.ImageField(required=False)

    class Meta:
        model = Persona
        fields = [
            "user",
            "telefono",
            "direccion",
            "nombre",
            "apellido",
            "imagen_perfil",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        imagen_perfil = validated_data.pop("imagen_perfil", None)
        persona = Persona.objects.create(user=user, **validated_data)
        if imagen_perfil:
            self.upload_image_to_firebase(persona, imagen_perfil)
        return persona

    def update(self, instance, validated_data):
        imagen_perfil = validated_data.pop("imagen_perfil", None)
        if imagen_perfil:
            self.upload_image_to_firebase(instance, imagen_perfil)
        instance.telefono = validated_data.get("telefono", instance.telefono)
        instance.direccion = validated_data.get("direccion", instance.direccion)
        instance.nombre = validated_data.get("nombre", instance.nombre)
        instance.apellido = validated_data.get("apellido", instance.apellido)
        instance.save()
        return instance


# Organizacion
class OrganizacionSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Organizacion
        fields = [
            "user",
            "telefono",
            "direccion",
            "rut_emp",
            "razon_social",
            "telefono2",
            "imagen_perfil",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        organizacion = Organizacion.objects.create(user=user, **validated_data)
        return organizacion

    def update(self, instance, validated_data):
        imagen_perfil = validated_data.pop("imagen_perfil", None)
        if imagen_perfil:
            self.upload_image_to_firebase(instance, imagen_perfil)
        instance.telefono = validated_data.get("telefono", instance.telefono)
        instance.direccion = validated_data.get("direccion", instance.direccion)
        instance.rut_emp = validated_data.get("rut_emp", instance.rut_emp)
        instance.razon_social = validated_data.get(
            "razon_social", instance.razon_social
        )
        instance.telefono2 = validated_data.get("telefono2", instance.telefono2)
        instance.save()

        return instance


# Administrador
class AdministradorSerializer(serializers.ModelSerializer):
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
        user = User.objects.create_superuser(**user_data)
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
