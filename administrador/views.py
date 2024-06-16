from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from api.models import Persona, Organizacion
from api.serializers import PersonaSerializer, OrganizacionSerializer
from .serializers import AdministradorSerializer


class RegistroAdmin(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AdministradorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Usuario Administrador registrado exitosamente."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersListCreate(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [IsAdminUser]


class PersDetail(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        serializer = None

        try:
            persona = Persona.objects.get(pk=pk)
            serializer = PersonaSerializer(persona)
            return Response(serializer.data)
        except Persona.DoesNotExist:
            return Response(
                {"message": "La persona no existe"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            persona = Persona.objects.get(pk=pk)
            persona.delete()
            return Response({"message": "Persona Eliminada con exito"})
        except Persona.DoesNotExist:
            return Response(
                {"message": "La persona no existe"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrgListCreate(generics.ListCreateAPIView):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer
    permission_classes = [IsAdminUser]


class OrgDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        serializer = None

        try:
            organizacion = Organizacion.objects.get(pk=pk)
            serializer = OrganizacionSerializer(organizacion)
            return Response(serializer.data)
        except Organizacion.DoesNotExist:
            return Response(
                {"message": "La organizacion no existe"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            organizacion = Organizacion.objects.get(pk=pk)
            organizacion.delete()
            return Response({"message": "Organizacion Eliminada con exito"})
        except Organizacion.DoesNotExist:
            return Response(
                {"message": "La organizacion no existe"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
