from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuarioSerializer
from .models import Usuario

class UsuarioView(APIView):

    # GET: obtener todos los usuarios
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response({"usuarios": serializer.data}, status=status.HTTP_200_OK)



    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)

        if serializer.is_valid():
            usuario = serializer.save()

            return Response(
                {
                    "mensaje": "Usuario registrado correctamente",
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "correo": usuario.correo
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

