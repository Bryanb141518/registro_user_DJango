from django.contrib import admin
from .models import Usuario # Usa el nombre real de tu clase aquí

admin.site.register(Usuario)
# Cambia el título de la pestaña del navegador
admin.site.site_title = "Mi Sistema de Datos"
admin.site.site_title = "Mi Sistema de Datos"
admin.site.index_title = "Bienvenido a la Tabla de Datos"