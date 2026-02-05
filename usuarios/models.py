from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

# creacion de la clase de usuario para que el sistema cree el usario con esto parametros
class UsuarioManager(BaseUserManager):
    def _create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('el correo es obligatorio')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)

        #hashea la contrasena nunca guarda terxto plano

        user.set_password(password)

        # guardar el usario en la bd aca el usario nace oficilamente
        user.save(using=self._db)
        return user
    # creacion del super usuario desde la terminal no permite correo de la bd
    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        #le da todos los permisos del sistema
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(correo, password, **extra_fields)

    # validacion de los datos como modelo de negocio
class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    edad = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )
    # valida que tenga el formato de correo prohibir que existan dos usario con el mismo correo
    correo = models.EmailField(unique=True)

    # activar y desactivar usuario
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #cambiar el modelo de usario por defecto y coloca el que delcaro par alas peticiones con bd
    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'  # Usar correo como username
    REQUIRED_FIELDS = ['nombre', 'apellido', 'edad']

    # definicionde como se van a mostrar los datos
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.correo