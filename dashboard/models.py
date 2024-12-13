from django.db import models
from django.contrib.auth.models import AbstractUser

from users.models import User


# Ubicación
class Ubicacion(models.Model):
    nombre = models.CharField(max_length=255, help_text="Nombre de la ubicación o área")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción adicional de la ubicación")
    municipio = models.CharField(max_length=255, help_text="Municipio relacionado")
    lat = models.CharField(max_length=255, blank=True, null=True, help_text="Latitud de la ubicación")
    lng = models.CharField(max_length=255, blank=True, null=True, help_text="Longitud de la ubicación")

    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"

    def __str__(self):
        return self.nombre


# Residuos
class Residuo(models.Model):
    fecha = models.DateField()
    cantidad_recolectada = models.FloatField(help_text="Cantidad de residuos recolectados en kg")
    cantidad_generada = models.FloatField(help_text="Cantidad total de residuos generados en kg")
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, blank=True, related_name='residuos')
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='residuos')

    class Meta:
        verbose_name = "Residuo"
        verbose_name_plural = "Residuos"
        ordering = ['fecha']

    def __str__(self):
        return f"Residuos del {self.fecha}"

    def tasa_recoleccion(self):
        if self.cantidad_generada > 0:
            return self.cantidad_recolectada / self.cantidad_generada
        return 0


# Eficiencia
class Eficiencia(models.Model):
    fecha = models.DateField()
    cantidad_gestionada = models.FloatField(help_text="Cantidad de residuos gestionados adecuadamente en kg")
    cantidad_generada = models.FloatField(help_text="Cantidad total de residuos generados en kg")
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, blank=True, related_name='eficiencia')
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='eficiencia')

    class Meta:
        verbose_name = "Nivel de Eficiencia"
        verbose_name_plural = "Niveles de Eficiencia"
        ordering = ['fecha']

    def __str__(self):
        return f"Eficiencia del {self.fecha}"

    def nivel_eficiencia(self):
        if self.cantidad_generada > 0:
            return self.cantidad_gestionada / self.cantidad_generada
        return 0


# Reutilización
class Reutilizacion(models.Model):
    fecha = models.DateField()
    cantidad_reutilizada = models.FloatField(help_text="Cantidad de residuos reutilizados en kg")
    cantidad_generada = models.FloatField(help_text="Cantidad total de residuos generados en kg")
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='reutilizacion')
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='reutilizacion')

    class Meta:
        verbose_name = "Tasa de Reutilización"
        verbose_name_plural = "Tasas de Reutilización"
        ordering = ['fecha']

    def __str__(self):
        return f"Reutilización del {self.fecha}"

    def tasa_reutilizacion(self):
        if self.cantidad_generada > 0:
            return self.cantidad_reutilizada / self.cantidad_generada
        return 0


# Vehículos
class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True, help_text="Placa única del vehículo")
    tipo = models.CharField(max_length=50, help_text="Tipo de vehículo (camión, camioneta, etc.)")
    capacidad = models.FloatField(help_text="Capacidad máxima de carga en kg")
    activo = models.BooleanField(default=True, help_text="Define si el vehículo está activo")

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"

    def __str__(self):
        return f"Vehículo {self.placa}"


# Rutas
class Ruta(models.Model):
    nombre = models.CharField(max_length=255, help_text="Nombre de la ruta")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción de la ruta")
    ubicaciones = models.ManyToManyField(Ubicacion, related_name='rutas',
                                         help_text="Ubicaciones incluidas en esta ruta")
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True, related_name='rutas')

    class Meta:
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"

    def __str__(self):
        return self.nombre


# Incidencias
class Incidencia(models.Model):
    fecha = models.DateField()
    descripcion = models.TextField(help_text="Descripción de la incidencia")
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='incidencias')
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidencias')

    class Meta:
        verbose_name = "Incidencia"
        verbose_name_plural = "Incidencias"
        ordering = ['-fecha']

    def __str__(self):
        return f"Incidencia en {self.ubicacion} el {self.fecha}"


# Reportes
class Reporte(models.Model):
    titulo = models.CharField(max_length=255, help_text="Título del reporte")
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción o resumen del reporte")
    datos = models.JSONField(help_text="Datos asociados al reporte (JSON)")
    generado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reportes')

    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"
        ordering = ['-fecha_generacion']

    def __str__(self):
        return f"Reporte: {self.titulo} ({self.fecha_generacion})"


class Recoleccion(models.Model):
    fecha = models.DateField()
    cantidad_recolectada = models.FloatField(help_text="Cantidad de residuos recolectados en kg")
    ruta = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True, blank=True, related_name='recolecciones')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='recolecciones')
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='recolecciones')

    class Meta:
        verbose_name = "Recolección"
        verbose_name_plural = "Recolecciones"
        ordering = ['fecha']

    def __str__(self):
        return f"Recolección el {self.fecha} en {self.ruta.nombre if self.ruta else 'sin ruta'}"

