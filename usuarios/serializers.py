from rest_framework import serializers
from .models import Usuario
#modulo de expresiones irregulares
import re
# crear un hassh para que la contrasena no se guarde tal cual sino como un algoritmo
from django.contrib.auth.hashers import make_password

# validacion del nombre
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre','apellido','edad','correo','password']

    def validate_nombre(self,value):
        #eliminacion de los espacios vacios al principio y al final de la palabra
        value = value.strip()
        #validacion de que no dejen el espacio vacio
        if not value:
            raise serializers.ValidationError('el nombre es obligatorio')

        #validar que en ninguna parte del nombre contenga numeros
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError('el nombre no puede llevar numeros ')

        # validacion de que no contenga ningun caracter especial si algo es incorrecto entra al for
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError(
                'El nombre solo puede contener letras y espacios'
            )

        # formato de envio la primera letra en mayuscula las demas en minuscula

        value = value.lower().capitalize()
        return value

    # validacion de apeliido
    def validate_apellido(self,value):
        # eliminacion de los espacios vacios al principio y al final de la palabra
        value = value.strip()
        # validacion de que no dejen el espacio vacio
        if not value:
            raise serializers.ValidationError('el apellido  es obligatorio')

        # validar que en ninguna parte del nombre contenga numeros
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError('el apellido no puede llevar numeros ')

        # validacion de que no contenga ningun caracter especial si algo es incorrecto entra al for
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError(
                'El apellido solo puede contener letras y espacios'
            )

        # formato de envio la primera letra en mayuscula las demas en minuscula

        value = value.lower().capitalize()
        # se genera el return por que por defecto la funcion tiene none
        return value

    #validacion de la edad
    def validate_edad(self,value):

        #no se valida nada mas por que la funcion que se crea en el model ya valida eso

        # el modelo ya valida:
        # que sea obligatorio
        # que sea entero
        # que sea positivo

        #validacion de que edad no sea mayor a 120
        if value > 120:
            raise serializers.ValidationError(
                'la edad no puede ser mayor a 120'
            )
        # se genera el return por que por defecto la funcion tiene none
        return value

    #validacion de correo
    def validate_correo(self,value):
        # eliminacion de los espacios vacios al principio y al final del dato
        value = value.strip()

        # si quieres un mensaje personalizado para obligatorio
        if not value:
            raise serializers.ValidationError('El correo es obligatorio')

        #validacion de que correo es obligatorio
        if Usuario.objects.filter(correo=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado")
        # ya se valida en el model los siguentes errores
        # no puede ir vacio
        # se valida que tenga el formato de correo
        # verificacion de que no exista otra persona con el mismo correo

        return value

    # validacion de password
    def validate_password(self,value):
        # eliminacion de los espacios vacios al principio y al final del dato
        value = value.strip()

        #MODULO RE PARA VALIDAR EXPRESIONES MAS COMPLEJAS EN UNA SOLA LINEA

        #obligatorio
        if not value:
            raise serializers.ValidationError('El password es obligatorio')

        if len(value) < 8:
            raise serializers.ValidationError("la contrasena debe tener al menos 8 caracteres")

        if len(value) > 128:
            raise serializers.ValidationError("la contrasena debe tener maximo 128 caracteres")

        # se importa re que es un modulo de expresiones regulares
        # esto dice que caulquir digito del 0 al 9 es valido r'\d
        if not re.search(r'\d', value):
            raise serializers.ValidationError('La contraseña debe contener al menos un número')

        # al menos una letra mayúscula
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('La contraseña debe contener al menos una letra mayúscula')

        # al menos una letra minúscula
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError('La contraseña debe contener al menos una letra minúscula')

        # al menos un carácter especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError('La contraseña debe contener al menos un carácter especial')

        return value


    # VALIDACION DE MODELO DE NEGOCIO
    def validate(self, data):
        edad = data.get('edad')

        if edad < 14:
            raise serializers.ValidationError({
                'edad': "No puedes registrarte, debes tener al menos 14 años."
            })

        if 14 <= edad < 18:
            # Puede registrarse, pero aplicamos lógica de negocio adicional
            data['restriccion'] = "Registro con supervisión de tutor"

        return data

    # convertir la contrasena a hash antes de guardarla en la bvase de datos
    def create(self, validated_data):
        # Convertir la contraseña en hash antes de guardar
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

