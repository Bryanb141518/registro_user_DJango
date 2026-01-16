from rest_framework.test import APITestCase
from .models import Usuario


#validacion del serialise
class UsuarioIntegrationTest(APITestCase):
    """Test de integración para validar todos los usuarios"""

    def test_verificar_todos_correos_unicos(self):
        """Verificar que TODOS los usuarios en la BD tienen correos únicos"""

        # Obtener TODOS los usuarios de la base de datos
        todos_usuarios = Usuario.objects.all()

        # Obtener todos los correos
        correos = [usuario.correo for usuario in todos_usuarios]

        # Verificar que no hay duplicados
        correos_unicos = set(correos)

        # Si hay duplicados, el set será más pequeño que la lista
        self.assertEqual(
            len(correos),
            len(correos_unicos),
            f"Se encontraron correos duplicados. Total usuarios: {len(correos)}, Correos únicos: {len(correos_unicos)}"
        )

        # Verificar cada correo individualmente
        for correo in correos_unicos:
            count = Usuario.objects.filter(correo=correo).count()
            self.assertEqual(
                count,
                1,
                f"El correo '{correo}' aparece {count} veces en la base de datos"
            )

