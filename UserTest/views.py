from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class WelcomeView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        endpoints_user = {
            "login": "/user/login/",
            "registro persona": "/user/persona/registro/",
            "registro organizacion": "/user/organizacion/registro/",
            "activacion de cuenta": "/user/activate-account/",
            "perfil usuario (requiere token de auth)": "/user/perfil/",
            "recuperar contraseña": "user/recuperar/",
            "confirmacion de rec. contraseña": "/user/recuperar-confirmacion/",
        }
        endpoints_admin = {
            "registro administrador": "/admin-user/registro/",
            "listar-crear personas": "/admin-user/personas/",
            "actualizar-eliminar persona": "/admin-user/personas/<int:pk>/",
            "listar-crear organizacion": "/admin-user/org/",
            "actualizar-eliminar organizacion": "/admin-user/org/<int:pk>/",
        }
        endpoints = {
            "bienvenida": "/",
            "USUARIOS": endpoints_user,
            "ADMIN (requiere permisos de admin)": endpoints_admin,
        }
        message = "¡Bienvenido a la API Usuarios! Aquí están los endpoints disponibles:"
        return Response({"message": message, "endpoints": endpoints})
