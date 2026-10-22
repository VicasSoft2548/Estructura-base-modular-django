
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    list_display = (
        'correo',
        'username',
        'estado_cuenta',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    list_filter = (
        'estado_cuenta',
        'is_active',
        'is_staff',
        'is_superuser',
        'groups',
    )

    search_fields = ('correo', 'username')
    ordering = ('correo',)

    fieldsets = UserAdmin.fieldsets + (
        ('Datos de la cuenta', {
            'fields': (
                'estado_cuenta',
                'requiere_cambio_password',
                'fecha_activacion',
                'fecha_ultimo_cambio_password',
                'intentos_fallidos',
                'bloqueado_hasta',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos de la cuenta', {
            'fields': ('correo', 'estado_cuenta')
        }),
    )
