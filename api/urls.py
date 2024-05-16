from django.urls import path
from .views import (
    PerfilUsuario,
    RegistroPersona,
    ActivateAccount,
    LoginView,
    RegistroOrganizaicion,
)

urlpatterns = [
    path("persona/registro/", RegistroPersona.as_view(), name="persona-registro"),
    path(
        "Organizacion/registro/",
        RegistroOrganizaicion.as_view(),
        name="organizacion-registro",
    ),
    path("activate-account/", ActivateAccount.as_view(), name="activate-account"),
    path("login/", LoginView.as_view(), name="login"),
    path("perfil/", PerfilUsuario.as_view(), name="perfil"),
]
