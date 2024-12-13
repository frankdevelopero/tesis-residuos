from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('vehiculos', VehicleView.as_view(), name="vehicles"),
    path('vehiculos/<int:pk>/eliminar/', VehicleDeleteView.as_view(), name='vehiculo_eliminar'),
    path('ubicaciones', UbicacionView.as_view(), name='ubicaciones'),
    path('ubicaciones/<int:pk>/eliminar/', EliminarUbicacionView.as_view(), name='ubicacion_eliminar'),
    path('rutas', RutaView.as_view(), name='rutas'),
    path('rutas/<int:pk>/eliminar/', EliminarRutaView.as_view(), name='ruta_eliminar'),
    path('mapa', MapaView.as_view(), name='mapa'),
    path('eficiencia/', EficienciaView.as_view(), name='eficiencia'),
    path('eficiencia/<int:pk>/eliminar/', EficienciaDeleteView.as_view(), name='eficiencia_eliminar'),
    path('recoleccion/', RecoleccionView.as_view(), name='recoleccion'),
    path('recoleccion/eliminar/<int:pk>/', RecoleccionDeleteView.as_view(), name='recoleccion_eliminar'),
    path('reutilizacion/', ReutilizacionView.as_view(), name='reutilizacion'),
    path('reutilizacion/eliminar/<int:pk>/', ReutilizacionDeleteView.as_view(), name='reutilizacion_eliminar'),
    path('incidencia/', IncidenciaView.as_view(), name='incidencia'),
    path('incidencia/eliminar/<int:pk>/', IncidenciaDeleteView.as_view(), name='incidencia_eliminar'),

]
