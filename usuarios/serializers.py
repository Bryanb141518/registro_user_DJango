from rest_framework import serializers
from .models import Usuario


# validacion del nombre
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre','apellido','edad','correo','password']

    def validate_nombre(self,value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('el nombre es obligatorio')
        