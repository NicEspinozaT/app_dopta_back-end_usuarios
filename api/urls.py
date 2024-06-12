from django.urls import path
from .views import (
    PerfilUsuario,
    VerPerfil,
    RegistroPersona,
    ActivateAccount,
    LoginView,
    RegistroOrganizaicion,
    RecuPasswordRequest,
    RecuPasswordConfirm,
)

urlpatterns = [
    path("persona/registro/", RegistroPersona.as_view(), name="persona-registro"),
    path(
        "organizacion/registro/",
        RegistroOrganizaicion.as_view(),
        name="organizacion-registro",
    ),
    path("activate-account/", ActivateAccount.as_view(), name="activate-account"),
    path("login/", LoginView.as_view(), name="login"),
    path("perfil/", PerfilUsuario.as_view(), name="perfil"),
    path("<int:pk>/perfil", VerPerfil.as_view(), name="ver-perfil"),
    path("recuperar/", RecuPasswordRequest.as_view(), name="recuperar-contraseña"),
    path(
        "recuperar-confirmacion/",
        RecuPasswordConfirm.as_view(),
        name="recuperar-confirmacion",
    ),
]
