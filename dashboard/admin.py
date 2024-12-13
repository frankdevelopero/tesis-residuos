from django.contrib import admin

from dashboard.models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'tipo', 'capacidad', 'activo')
    search_fields = ('placa', 'tipo')
    list_filter = ('activo', 'tipo')
    list_editable = ('activo',)
    ordering = ('placa',)
    fieldsets = (
        ('Información del Vehículo', {
            'fields': ('placa', 'tipo', 'capacidad')
        }),
        ('Estado', {
            'fields': ('activo',),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.save()
    actions = ['marcar_como_activo', 'marcar_como_inactivo']

    def marcar_como_activo(self, request, queryset):
        queryset.update(activo=True)
        self.message_user(request, "Vehículos marcados como activos.")
    marcar_como_activo.short_description = "Marcar como activo"

    def marcar_como_inactivo(self, request, queryset):
        queryset.update(activo=False)
        self.message_user(request, "Vehículos marcados como inactivos.")
    marcar_como_inactivo.short_description = "Marcar como inactivo"
