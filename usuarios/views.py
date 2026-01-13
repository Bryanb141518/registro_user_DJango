from rest_framework.viewsets import ModelViewSet
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

