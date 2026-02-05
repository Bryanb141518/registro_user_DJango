from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .serializers import UsuarioSerializer
from .models import Usuario

# Mostrar la página web en el navegador
def index(request):
    return render(request, "index.html")

# ViewSet profesional - CRUD completo automático
class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
#declaracion de formato de ejecucion del test
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data

        # Agregar mensaje si la edad es menor a 18
        edad = serializer.validated_data.get('edad')
        if edad < 18:
            response_data['mensaje'] = "Puedes registrarte pero con ciertas restricciones"

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)