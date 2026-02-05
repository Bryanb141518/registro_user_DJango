from rest_framework.test import APITestCase
from rest_framework import status
from .models import Usuario

class UsuarioIntegrationTest(APITestCase):
    """Test de integración para usuarios"""

    def setUp(self):
        """Crear un usuario inicial en la BD de prueba"""
        self.usuario_existente = Usuario.objects.create(
            nombre="Maria",
            apellido="Lopez",
            edad=25,
            correo="maria@test.com",
            password="Password1!"
        )

# no se valida como integracion por que simplemente quiero validar que slate el error cuando encuentre otro igual
    def test_no_se_puede_crear_usuario_con_correo_duplicado(self):
        """Verifica que no se puede registrar un usuario con un correo ya existente"""

        data_duplicado = {
            "nombre": "Juan",
            "apellido": "Perez",
            "edad": 30,
            "correo": "maria@test.com",  # mismo correo que el usuario creado en setUp
            "password": "Password1!"
        }

        # Se hace POST al endpoint real de creación de usuarios
        response = self.client.post("/api/usuarios/api/", data_duplicado, format='json')  #  Correcto

        # Verificar que el status code sea 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verificar que el mensaje de error contenga la clave 'correo'
        self.assertIn("correo", response.data)

        # Verificar que el mensaje de error sea el esperado
        self.assertEqual(response.data["correo"][0], "Este correo ya está registrado")

    def test_edad_menor_a_14_no_se_puede_registrar(self):
        """Edad menor a 14 debe generar error"""
        data = {
            "nombre": "Juan",
            "apellido": "Perez",
            "edad": 12,  # menor a 14
            "correo": "juan12@test.com",
            "password": "Password1!"
        }

        response = self.client.post("/api/usuarios/api/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("edad", response.data)
        self.assertEqual(
            str(response.data["edad"][0]),
            "No puedes registrarte, debes tener al menos 14 años."
        )

    def test_edad_mayor_a_120_no_se_puede_registrar(self):
        """Edad mayor a 120 debe generar error"""
        data = {
            "nombre": "Pedro",
            "apellido": "Gomez",
            "edad": 150,  # mayor a 120
            "correo": "pedro150@test.com",
            "password": "Password1!"
        }

        response = self.client.post("/api/usuarios/api/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("edad", response.data)
        self.assertEqual(
            str(response.data["edad"][0]),
            "la edad no puede ser mayor a 120"
        )

    def test_edad_entre_14_y_17_muestra_restricciones(self):
        """Edad entre 14 y 17 pasa pero con mensaje de restricciones"""
        data = {
            "nombre": "Ana",
            "apellido": "Martinez",
            "edad": 16,  # entre 14 y 17
            "correo": "ana16@test.com",
            "password": "Password1!"
        }

        response = self.client.post("/api/usuarios/api/", data, format='json')

        # Debe pasar (201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # El mensaje de restricción se encuentra en la respuesta
        self.assertIn("mensaje", response.data)
        self.assertEqual(
            response.data["mensaje"],
            "Puedes registrarte pero con ciertas restricciones"
        )