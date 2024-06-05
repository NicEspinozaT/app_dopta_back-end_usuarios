from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from api.models import Persona, Organizacion
from api.serializers import PersonaSerializer, OrganizacionSerializer

"""
TODO: 
    - Agregar vista creacion de administrador
    con permiso Admin
"""


class PersListCreate(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [IsAdminUser]


class PersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [IsAdminUser]


class OrgListCreate(generics.ListCreateAPIView):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer
    permission_classes = [IsAdminUser]


class OrgDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer
    permission_classes = [IsAdminUser]
