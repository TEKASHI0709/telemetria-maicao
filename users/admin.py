from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, Recurso


class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('nombre', 'apellido', 'roles')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('nombre', 'apellido', 'roles')}),
    )
    list_display = ('username', 'email', 'nombre', 'apellido', 'is_staff', 'is_active')
    filter_horizontal = ('roles', 'groups', 'user_permissions')


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol)
admin.site.register(Recurso)