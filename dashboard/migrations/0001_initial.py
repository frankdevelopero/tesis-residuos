# Generated by Django 5.1.2 on 2024-12-04 00:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Nombre de la ubicación o área', max_length=255)),
                ('descripcion', models.TextField(blank=True, help_text='Descripción adicional de la ubicación', null=True)),
                ('municipio', models.CharField(help_text='Municipio relacionado', max_length=255)),
                ('lat', models.CharField(blank=True, help_text='Latitud de la ubicación', max_length=255, null=True)),
                ('lng', models.CharField(blank=True, help_text='Longitud de la ubicación', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Ubicación',
                'verbose_name_plural': 'Ubicaciones',
            },
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(help_text='Placa única del vehículo', max_length=10, unique=True)),
                ('tipo', models.CharField(help_text='Tipo de vehículo (camión, camioneta, etc.)', max_length=50)),
                ('capacidad', models.FloatField(help_text='Capacidad máxima de carga en kg')),
                ('activo', models.BooleanField(default=True, help_text='Define si el vehículo está activo')),
            ],
            options={
                'verbose_name': 'Vehículo',
                'verbose_name_plural': 'Vehículos',
            },
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(help_text='Título del reporte', max_length=255)),
                ('fecha_generacion', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.TextField(blank=True, help_text='Descripción o resumen del reporte', null=True)),
                ('datos', models.JSONField(help_text='Datos asociados al reporte (JSON)')),
                ('generado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reportes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reporte',
                'verbose_name_plural': 'Reportes',
                'ordering': ['-fecha_generacion'],
            },
        ),
        migrations.CreateModel(
            name='Reutilizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('cantidad_reutilizada', models.FloatField(help_text='Cantidad de residuos reutilizados en kg')),
                ('cantidad_generada', models.FloatField(help_text='Cantidad total de residuos generados en kg')),
                ('registrado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reutilizacion', to=settings.AUTH_USER_MODEL)),
                ('ubicacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reutilizacion', to='dashboard.ubicacion')),
            ],
            options={
                'verbose_name': 'Tasa de Reutilización',
                'verbose_name_plural': 'Tasas de Reutilización',
                'ordering': ['fecha'],
            },
        ),
        migrations.CreateModel(
            name='Residuo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('cantidad_recolectada', models.FloatField(help_text='Cantidad de residuos recolectados en kg')),
                ('cantidad_generada', models.FloatField(help_text='Cantidad total de residuos generados en kg')),
                ('registrado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='residuos', to=settings.AUTH_USER_MODEL)),
                ('ubicacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='residuos', to='dashboard.ubicacion')),
            ],
            options={
                'verbose_name': 'Residuo',
                'verbose_name_plural': 'Residuos',
                'ordering': ['fecha'],
            },
        ),
        migrations.CreateModel(
            name='Incidencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.TextField(help_text='Descripción de la incidencia')),
                ('responsable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incidencias', to=settings.AUTH_USER_MODEL)),
                ('ubicacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incidencias', to='dashboard.ubicacion')),
            ],
            options={
                'verbose_name': 'Incidencia',
                'verbose_name_plural': 'Incidencias',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='Eficiencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('cantidad_gestionada', models.FloatField(help_text='Cantidad de residuos gestionados adecuadamente en kg')),
                ('cantidad_generada', models.FloatField(help_text='Cantidad total de residuos generados en kg')),
                ('registrado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eficiencia', to=settings.AUTH_USER_MODEL)),
                ('ubicacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eficiencia', to='dashboard.ubicacion')),
            ],
            options={
                'verbose_name': 'Nivel de Eficiencia',
                'verbose_name_plural': 'Niveles de Eficiencia',
                'ordering': ['fecha'],
            },
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Nombre de la ruta', max_length=255)),
                ('descripcion', models.TextField(blank=True, help_text='Descripción de la ruta', null=True)),
                ('ubicaciones', models.ManyToManyField(help_text='Ubicaciones incluidas en esta ruta', related_name='rutas', to='dashboard.ubicacion')),
                ('vehiculo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rutas', to='dashboard.vehiculo')),
            ],
            options={
                'verbose_name': 'Ruta',
                'verbose_name_plural': 'Rutas',
            },
        ),
    ]
