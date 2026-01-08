from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Usuario


# ----------------------------
# pre_save: antes de guardar
# ----------------------------
@receiver(pre_save, sender=Usuario)
def formatear_nombre_apellido(sender, instance, **kwargs):
    """
    Se ejecuta antes de guardar un Usuario
    Formatea nombre y apellido: primera letra mayúscula, elimina espacios
    """
    if instance.nombre:
        instance.nombre = instance.nombre.strip().title()
    if instance.apellido:
        instance.apellido = instance.apellido.strip().title()


# ----------------------------
# post_save: después de guardar
# ----------------------------
@receiver(post_save, sender=Usuario)
def enviar_correo_bienvenida(sender, instance, created, **kwargs):
    """
    Se ejecuta después de guardar un Usuario
    Envía un correo de bienvenida si se creó un nuevo usuario
    """
    if created:
        asunto = "¡Bienvenido a MiApp!"
        mensaje = f"Hola {instance.nombre},\n\nGracias por registrarte en nuestra plataforma."
        destinatario = [instance.correo]  # email del usuario

        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=None,  # usará DEFAULT_FROM_EMAIL del settings
            recipient_list=destinatario,
            fail_silently=False,  # muestra error si algo falla
        )

        print(f"Correo de bienvenida enviado a {instance.correo}")
