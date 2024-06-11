from django.urls import path
from .views import PersListCreate, PersDetail, OrgListCreate, OrgDetail, RegistroAdmin

urlpatterns = [
    # URLs para personas
    path("registro/", RegistroAdmin.as_view(), name="registro-admin"),
    path("personas/", PersListCreate.as_view(), name="persona-list-create"),
    path("personas/<int:pk>/", PersDetail.as_view(), name="persona-detail"),
    # URLs para organizaciones
    path("org/", OrgListCreate.as_view(), name="org-list-create"),
    path("org/<int:pk>/", OrgDetail.as_view(), name="org-detail"),
]
