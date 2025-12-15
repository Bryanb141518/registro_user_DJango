from django.db import models

class Usuario(models.Model):
    # cantidad de caracteres y tipo de texto
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    # para evitar edades negativas
    edad =models.PositiveIntegerField()

    # con esto indicamos que el correo debe de ser por que el correo es como el id del usario
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=128)



