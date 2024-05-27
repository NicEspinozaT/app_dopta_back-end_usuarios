from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    PersonaSerializer,
    LoginSerializer,
    OrganizacionSerializer,
    AdministradorSerializer,
    RecuPassRequestserializer,
    RecuPassConfirmserializer,
)
from django.contrib.auth.tokens import default_token_generator
from .models import User, Persona, Organizacion, Administrador


# login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    if user.is_active:
                        user.last_login = timezone.now()
                        user.save(update_fields=["last_login"])
                        refresh = RefreshToken.for_user(user)
                        access = refresh.access_token
                        return Response(
                            {"access": str(access), "refresh": str(refresh)}
                        )
                    else:
                        # Generar token de activación
                        token = default_token_generator.make_token(user)
                        activation_link = (
                            settings.BASE_URL
                            + reverse("activate-account")
                            + f"?email={user.email}&token={token}"
                        )
                        subject = "Activación de cuenta"
                        message = f"Por favor, haz clic en el siguiente enlace para activar tu cuenta: {activation_link}"
                        send_mail(
                            subject, message, settings.EMAIL_HOST_USER, [user.email]
                        )
                        return Response(
                            {
                                "error": "La cuenta está desactivada, se reenviara un correo con el nuevo link de actualizacion"
                            },
                            status=status.HTTP_403_FORBIDDEN,
                        )
                else:
                    return Response(
                        {"error": "Credenciales Invalidas"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except User.DoesNotExist:
                return Response(
                    {"error": "Usuario no encontrado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Registro persona
class RegistroPersona(APIView):
    def post(self, request):
        serializer = PersonaSerializer(data=request.data)
        if serializer.is_valid():
            persona = serializer.save()

            # Generar token de activación
            token = default_token_generator.make_token(persona.user)
            activation_link = (
                settings.BASE_URL
                + reverse("activate-account")
                + f"?email={persona.user.email}&token={token}&user_type=Persona"
            )
            subject = "Activación de cuenta"
            message = f"Por favor, haz clic en el siguiente enlace para activar tu cuenta: {activation_link}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [persona.user.email])

            return Response(
                {
                    "message": "Usuario registrado exitosamente. Se ha enviado un correo electrónico de activación."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Registro organizacion
class RegistroOrganizaicion(APIView):
    def post(self, request):
        serializer = OrganizacionSerializer(data=request.data)
        if serializer.is_valid():
            organizacion = serializer.save()

            # Generar token de activación
            token = default_token_generator.make_token(organizacion.user)
            activation_link = (
                settings.BASE_URL
                + reverse("activate-account")
                + f"?email={organizacion.user.email}&token={token}&user_type=Organizacion"
            )
            subject = "Activación de cuenta"
            message = f"Por favor, haz clic en el siguiente enlace para activar tu cuenta: {activation_link}"
            send_mail(
                subject, message, settings.EMAIL_HOST_USER, [organizacion.user.email]
            )

            return Response(
                {
                    "message": "Usuario registrado exitosamente. Se ha enviado un correo electrónico de activación."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PerfilUsuario(APIView):
    # Método para obtener el perfil de usuario
    def get(self, request):
        user = request.user

        # Inicializar el objeto de datos y el serializer
        data = {}
        serializer = None

        if Persona.objects.filter(user=user).exists():

            perfil_persona = Persona.objects.get(user=user)
            serializer = PersonaSerializer(perfil_persona)
        elif Organizacion.objects.filter(user=user).exists():
            perfil_organizacion = Organizacion.objects.get(user=user)
            serializer = OrganizacionSerializer(perfil_organizacion)
        elif Administrador.objects.filter(user=user).exists():

            perfil_administrador = Administrador.objects.get(user=user)
            serializer = AdministradorSerializer(perfil_administrador)
        else:
            return Response(
                {"error": "No se encontró ningún perfil asociado al usuario."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serializar los datos del perfil y retornar la respuesta
        if serializer:
            data = serializer.data
            return Response(data)

    # Método para actualizar el perfil de usuario
    def put(self, request):
        user = request.user

        # Determinar el tipo de submodelo asociado al usuario
        if Persona.objects.filter(user=user).exists():
            perfil_persona = Persona.objects.get(user=user)
            serializer = PersonaSerializer(
                perfil_persona, data=request.data, partial=True
            )
        elif Organizacion.objects.filter(user=user).exists():
            perfil_organizacion = Organizacion.objects.get(user=user)
            serializer = OrganizacionSerializer(
                perfil_organizacion, data=request.data, partial=True
            )
        elif Administrador.objects.filter(user=user).exists():
            perfil_administrador = Administrador.objects.get(user=user)
            serializer = AdministradorSerializer(
                perfil_administrador, data=request.data, partial=True
            )
        else:
            return Response(
                {"error": "No se encontró ningún perfil asociado al usuario."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validar y guardar los datos actualizados del perfil
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Activacion cuenta
class ActivateAccount(APIView):
    permission_classes = []

    def get(self, request):
        email = request.GET.get("email")
        token = request.GET.get("token")

        # Verificar el token y activar la cuenta
        try:
            user = User.objects.get(email=email)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                # print(user.persona.data)
                return Response(
                    {"message": "¡Tu cuenta ha sido activada correctamente!"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Token de activación inválido."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except user.DoesNotExist:
            return Response(
                {"error": "No se encontró ningún usuario con ese correo electrónico."},
                status=status.HTTP_404_NOT_FOUND,
            )


# Recuperacion contraseña
class RecuPasswordRequest(APIView):
    def post(self, request):
        serializer = RecuPassRequestserializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)
            if user:
                token = default_token_generator.make_token(user)
                reset_url = reverse("recuperar-confirmacion")
                reset_url += f"?email={email}&token={token}"
                reset_link = settings.BASE_URL + reset_url
                subject = "Recuperación de Contraseña"
                message = f"Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_link}"
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                return Response(
                    {
                        "message": "Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña."
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "error": "No se encontró ningún usuario con ese correo electrónico."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecuPasswordConfirm(APIView):
    def post(self, request):
        serializer = RecuPassConfirmserializer(data=request.data)
        if serializer.is_valid():
            email = request.GET.get("email")
            token = request.GET.get("token")
            new_password = serializer.validated_data["new_password"]
            try:
                user = User.objects.get(email=email)
                if user and default_token_generator.check_token(user, token):

                    user.password = new_password
                    user.save()
                    user.set_password(user.password)
                    return Response(
                        {"message": "La contraseña se ha restablecido correctamente."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "Token de restablecimiento de contraseña inválido."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except:
                return Response({"error": "Link invalido!!!"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
