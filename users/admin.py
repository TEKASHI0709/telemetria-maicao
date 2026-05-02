from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, Recurso

admin.site.register(Usuario, UserAdmin)
admin.site.register(Rol)
admin.site.register(Recurso)