from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Usuario

@receiver(post_save, sender=Usuario)
def usuario_creado(sender, instance, created, **kwargs):
    """
    Signal que se ejecuta después de guardar un Usuario
    """
    if created:
        print(f"Nuevo usuario creado: {instance.nombre} {instance.apellido}")
        print(f"Email: {instance.correo}")
        print(f"Edad: {instance.edad}")
        # Aquí puedes agregar más lógica:
        # - Enviar email de bienvenida
        # - Crear perfil automáticamente
        # - Registrar en logs
        # - Notificar a administradores

@receiver(pre_save, sender=Usuario)
def antes_guardar_usuario(sender, instance, **kwargs):
    """
    Signal que se ejecuta antes de guardar un Usuario
    """
    # Formatear nombre y apellido automáticamente
    if instance.nombre:
        instance.nombre = instance.nombre.strip().title()
    if instance.apellido:
        instance.apellido = instance.apellido.strip().title()
    
    print(f"Preparando para guardar usuario: {instance.nombre} {instance.apellido}")
    
    # Aquí puedes agregar más lógica:
    # - Validaciones adicionales
    # - Formateo de datos
    # - Auditoría de cambios