from django.urls import path
from .views import PersListCreate, PersDetail, OrgListCreate, OrgDetail, RegistroAdmin

urlpatterns = [
    # URLs para personas
    path("admin/registro/", RegistroAdmin.as_view(), name="registro-admin"),
    path("admin/personas/", PersListCreate.as_view(), name="persona-list-create"),
    path("admin/personas/<int:pk>/", PersDetail.as_view(), name="persona-detail"),
    # URLs para organizaciones
    path("admin/org/", OrgListCreate.as_view(), name="org-list-create"),
    path("admin/org/<int:pk>/", OrgDetail.as_view(), name="org-detail"),
]
