from django import forms
from dashboard.models import Vehiculo, Ubicacion, Ruta, Eficiencia, Recoleccion, Reutilizacion, Incidencia
from users.models import User


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'tipo', 'capacidad']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['nombre', 'descripcion', 'municipio', 'lat', 'lng']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '', 'rows': 3}),
            'municipio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'lat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'readonly': 'readonly'}),
            'lng': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'readonly': 'readonly'}),
        }


class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = ['nombre', 'descripcion', 'ubicaciones', 'vehiculo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la ruta'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'ubicaciones': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Puedes personalizar los textos de los campos si es necesario
        self.fields['ubicaciones'].queryset = Ubicacion.objects.all()
        self.fields['vehiculo'].queryset = Vehiculo.objects.filter(activo=True)


class EficienciaForm(forms.ModelForm):
    class Meta:
        model = Eficiencia
        fields = ['fecha', 'cantidad_gestionada', 'cantidad_generada', 'ubicacion', 'registrado_por']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cantidad_gestionada': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad gestionada'}),
            'cantidad_generada': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad generada'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'registrado_por': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ubicacion'].queryset = Ubicacion.objects.all()
        self.fields['registrado_por'].queryset = User.objects.all()


class RecoleccionForm(forms.ModelForm):
    class Meta:
        model = Recoleccion
        fields = ['fecha', 'cantidad_recolectada', 'ruta', 'vehiculo', 'registrado_por']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cantidad_recolectada': forms.NumberInput(attrs={'class': 'form-control'}),
            'ruta': forms.Select(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'registrado_por': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ruta'].queryset = Ruta.objects.all()
        self.fields['vehiculo'].queryset = Vehiculo.objects.filter(activo=True)
        self.fields['registrado_por'].queryset = User.objects.all()


class ReutilizacionForm(forms.ModelForm):
    class Meta:
        model = Reutilizacion
        fields = ['fecha', 'cantidad_reutilizada', 'cantidad_generada', 'ubicacion', 'registrado_por']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cantidad_reutilizada': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_generada': forms.NumberInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'registrado_por': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ubicacion'].queryset = Ubicacion.objects.all()
        self.fields['registrado_por'].queryset = User.objects.all()


class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ['fecha', 'descripcion', 'ubicacion', 'responsable']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ubicacion'].queryset = Ubicacion.objects.all()
        self.fields['responsable'].queryset = User.objects.all()




