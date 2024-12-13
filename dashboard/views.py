import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.db.models import Sum, Count
from dashboard.forms import VehiculoForm, UbicacionForm, RutaForm, EficienciaForm, RecoleccionForm, ReutilizacionForm, \
    IncidenciaForm
from dashboard.models import Vehiculo, Ubicacion, Ruta, Eficiencia, Recoleccion, Reutilizacion, Incidencia


class DashboardView(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {
            'total_recolecciones': Recoleccion.objects.count(),
            'recolecciones_programadas': Recoleccion.objects.filter(fecha__gte=datetime.date.today()).count(),
            'residuos_recolectados': Recoleccion.objects.aggregate(
                Sum('cantidad_recolectada'))['cantidad_recolectada__sum'] or 0,
            'incidencias_reportadas': Incidencia.objects.count(),
            'niveles_eficiencia': Eficiencia.objects.count(),
            'tasas_reutilizacion': Reutilizacion.objects.count(),
            'vehiculos_activos': Vehiculo.objects.filter(activo=True).count(),
            'rutas_disponibles': Ruta.objects.count(),
        }
        return render(request, 'dashboard/index.html', context)



class VehicleView(View):
    @method_decorator(login_required())
    def get(self, request):
        vehiculos = Vehiculo.objects.filter(activo=True)
        form = VehiculoForm()
        context = {'vehiculos': vehiculos, 'form': form}
        return render(request, 'dashboard/vehiculos.html', context)

    @method_decorator(login_required())
    def post(self, request):
        vehiculo_id = request.POST.get('vehiculo_id')
        if vehiculo_id:
            vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
            form = VehiculoForm(request.POST, instance=vehiculo)
        else:
            form = VehiculoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('vehicles')
        vehiculos = Vehiculo.objects.filter(activo=True)
        context = {'vehiculos': vehiculos, 'form': form, 'editing': bool(vehiculo_id)}
        return render(request, 'dashboard/vehiculos.html', context)


class VehicleDeleteView(View):
    @method_decorator(login_required())
    def post(self, request, pk):
        vehiculo = get_object_or_404(Vehiculo, pk=pk)
        vehiculo.delete()
        return redirect('vehicles')


class UbicacionView(View):
    @method_decorator(login_required)
    def get(self, request):
        ubicaciones = Ubicacion.objects.all()
        form = UbicacionForm()
        context = {'ubicaciones': ubicaciones, 'form': form}
        return render(request, 'dashboard/ubicaciones.html', context)

    @method_decorator(login_required)
    def post(self, request):
        ubicacion_id = request.POST.get('ubicacion_id')
        if ubicacion_id:
            ubicacion = get_object_or_404(Ubicacion, pk=ubicacion_id)
            form = UbicacionForm(request.POST, instance=ubicacion)
        else:
            form = UbicacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ubicaciones')
        ubicaciones = Ubicacion.objects.all()
        context = {'ubicaciones': ubicaciones, 'form': form, 'editing': bool(ubicacion_id)}
        return render(request, 'dashboard/ubicaciones.html', context)


class EliminarUbicacionView(View):
    @method_decorator(login_required())
    def post(self, request, pk):
        ubicacion = get_object_or_404(Ubicacion, pk=pk)
        ubicacion.delete()
        return redirect('ubicaciones')


class RutaView(View):
    @method_decorator(login_required)
    def get(self, request):
        rutas = Ruta.objects.all()
        form = RutaForm()
        context = {'rutas': rutas, 'form': form}
        return render(request, 'dashboard/rutas.html', context)

    @method_decorator(login_required)
    def post(self, request):
        ruta_id = request.POST.get('ruta_id')
        if ruta_id:  # Edición
            ruta = get_object_or_404(Ruta, pk=ruta_id)
            form = RutaForm(request.POST, instance=ruta)
        else:  # Creación
            form = RutaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('rutas')

        rutas = Ruta.objects.all()
        context = {'rutas': rutas, 'form': form, 'editing': bool(ruta_id)}
        return render(request, 'dashboard/rutas.html', context)


class EliminarRutaView(View):
    @method_decorator(login_required())
    def post(self, request, pk):
        ruta = get_object_or_404(Ruta, pk=pk)
        ruta.delete()
        return redirect('rutas')


class MapaView(View):
    @method_decorator(login_required)
    def get(self, request):
        rutas = Ruta.objects.all()
        context = {'rutas': rutas}
        return render(request, 'dashboard/mapa.html', context)


class EficienciaView(View):
    @method_decorator(login_required)
    def get(self, request):
        eficiencia_list = Eficiencia.objects.all()
        form = EficienciaForm()
        context = {'eficiencia_list': eficiencia_list, 'form': form}
        return render(request, 'dashboard/eficiencia.html', context)

    @method_decorator(login_required)
    def post(self, request):
        eficiencia_id = request.POST.get('eficiencia_id')
        if eficiencia_id:
            eficiencia = get_object_or_404(Eficiencia, pk=eficiencia_id)
            form = EficienciaForm(request.POST, instance=eficiencia)
        else:
            form = EficienciaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('eficiencia')

        eficiencia_list = Eficiencia.objects.all()
        context = {'eficiencia_list': eficiencia_list, 'form': form, 'editing': bool(eficiencia_id)}
        return render(request, 'dashboard/eficiencia.html', context)


class EficienciaDeleteView(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        eficiencia = get_object_or_404(Eficiencia, pk=pk)
        eficiencia.delete()
        return redirect('eficiencia')


class RecoleccionView(View):
    @method_decorator(login_required)
    def get(self, request):
        recoleccion_list = Recoleccion.objects.all()
        form = RecoleccionForm()
        context = {'recoleccion_list': recoleccion_list, 'form': form}
        return render(request, 'dashboard/recoleccion.html', context)

    @method_decorator(login_required)
    def post(self, request):
        recoleccion_id = request.POST.get('recoleccion_id')
        if recoleccion_id:
            recoleccion = get_object_or_404(Recoleccion, pk=recoleccion_id)
            form = RecoleccionForm(request.POST, instance=recoleccion)
        else:
            form = RecoleccionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('recoleccion')

        recoleccion_list = Recoleccion.objects.all()
        context = {'recoleccion_list': recoleccion_list, 'form': form, 'editing': bool(recoleccion_id)}
        return render(request, 'dashboard/recoleccion.html', context)


class RecoleccionDeleteView(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        recoleccion = get_object_or_404(Recoleccion, pk=pk)
        recoleccion.delete()
        return redirect('recoleccion')


class ReutilizacionView(View):
    @method_decorator(login_required)
    def get(self, request):
        reutilizacion_list = Reutilizacion.objects.all()
        form = ReutilizacionForm()
        context = {'reutilizacion_list': reutilizacion_list, 'form': form}
        return render(request, 'dashboard/reutilizacion.html', context)

    @method_decorator(login_required)
    def post(self, request):
        reutilizacion_id = request.POST.get('reutilizacion_id')
        if reutilizacion_id:
            reutilizacion = get_object_or_404(Reutilizacion, pk=reutilizacion_id)
            form = ReutilizacionForm(request.POST, instance=reutilizacion)
        else:
            form = ReutilizacionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('reutilizacion')

        reutilizacion_list = Reutilizacion.objects.all()
        context = {'reutilizacion_list': reutilizacion_list, 'form': form, 'editing': bool(reutilizacion_id)}
        return render(request, 'dashboard/reutilizacion.html', context)


class ReutilizacionDeleteView(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        reutilizacion = get_object_or_404(Reutilizacion, pk=pk)
        reutilizacion.delete()
        return redirect('reutilizacion')


class IncidenciaView(View):
    @method_decorator(login_required)
    def get(self, request):
        incidencia_list = Incidencia.objects.all()
        form = IncidenciaForm()
        context = {'incidencia_list': incidencia_list, 'form': form}
        return render(request, 'dashboard/incidencia.html', context)

    @method_decorator(login_required)
    def post(self, request):
        incidencia_id = request.POST.get('incidencia_id')
        if incidencia_id:
            incidencia = get_object_or_404(Incidencia, pk=incidencia_id)
            form = IncidenciaForm(request.POST, instance=incidencia)
        else:
            form = IncidenciaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('incidencia')

        incidencia_list = Incidencia.objects.all()
        context = {'incidencia_list': incidencia_list, 'form': form, 'editing': bool(incidencia_id)}
        return render(request, 'dashboard/incidencia.html', context)


class IncidenciaDeleteView(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        incidencia = get_object_or_404(Incidencia, pk=pk)
        incidencia.delete()
        return redirect('incidencia')




