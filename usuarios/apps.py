from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    name = 'usuarios'
    verbose_name = 'Gestión de Clientes'
    
    def ready(self):
        """
        Se ejecuta cuando Django carga la aplicación
        Aquí importamos los signals para que se registren
        """
        import usuarios.signals

        