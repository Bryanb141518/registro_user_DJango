from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import UsuarioSerializer
from .models import Usuario

#mostrar la pagina web en el navegador
def index(request):
    return render(request, "index.html")
# para ignorar el token que se debe pasa en js e ir directamente a saber que meto utilizar
@method_decorator(csrf_exempt, name='dispatch')
class UsuarioView(APIView):

    # GET: obtener todos los usuarios o uno específico por ID
    def get(self, request, id=None):
        if id:
            # GET /api/usuarios/5/ → Un usuario específico
            try:
                usuario = Usuario.objects.get(id=id)
                serializer = UsuarioSerializer(usuario)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Usuario.DoesNotExist:
                return Response(
                    {"error": "Usuario no encontrado"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # GET /api/usuarios/ → Todos los usuarios
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


    def put(self, request, id):
        try:
            usuario = Usuario.objects.get(id=id)
        except Usuario.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
# se crea la variable y se llama a la clase usuario se llama a la varible de try y de entregan los datos
# que pase los datos  al serilize y con portial va a remplazar los datos que el usario mande

        serializer = UsuarioSerializer(
            usuario,
            data=request.data,
            partial=True  # permite actualizar solo algunos campos
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"mensaje": "Usuario actualizado correctamente"},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        try:
            usuario = Usuario.objects.get(id=id)
            usuario.delete()
            return Response(
                {"mensaje": "Usuario eliminado correctamente"},
                status=status.HTTP_200_OK
            )
        except Usuario.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

