from django.contrib import admin
from .models import Persona, Organizacion, Administrador, Usuario

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Persona)
admin.site.register(Organizacion)
admin.site.register(Administrador)
