import sys  # Importa el módulo sys
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime
import os
import pytz
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .models import (AnalisisAcelerometro, AnalisisTemperatura, AnalisisFrecuenciaCardiaca,
                     AnalisisBVP, AnalisisIBI, Usuario)
from .forms import ArchivoForm
from statistics import mean, median

# Define la zona horaria UTC
utc = pytz.UTC

def captura_file(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('loading'))
    else:
        formulario = ArchivoForm()
    return render(request, 'upload.html', {'form': formulario})

def loading_view(request):
    return render(request, 'loading.html')

def procesar_archivos(request):
    if request.method == 'POST':
        formulario = ArchivoForm(request.POST, request.FILES)
        if formulario.is_valid():
            fs = FileSystemStorage()
            contexto = {'form': formulario}

            nombre = formulario.cleaned_data['nombre']
            edad = formulario.cleaned_data['edad']
            usuario, created = Usuario.objects.get_or_create(nombre=nombre, edad=edad)

            with ThreadPoolExecutor() as executor:
                futures = []
                file_keys = ['temp', 'hr', 'acc', 'bvp', 'ibi']
                for key in file_keys:
                    file_field_name = f'archivo_{key}'
                    archivo = request.FILES.get(file_field_name)
                    if archivo:
                        func_name = f'procesar_archivo_{key}'
                        if hasattr(sys.modules[__name__], func_name):
                            func = getattr(sys.modules[__name__], func_name)
                            futures.append(executor.submit(func, archivo, fs, usuario))

                for future in futures:
                    resultado = future.result()
                    contexto.update(resultado)

            return render(request, 'upload.html', contexto)
    else:
        formulario = ArchivoForm()
    return render(request, 'upload.html', {'form': formulario})

def procesar_archivo_generico(archivo, fs, usuario, tipo_dato):
    nombre_archivo = fs.save(archivo.name, archivo)
    ruta_archivo = fs.path(nombre_archivo)
    with open(ruta_archivo, 'r') as file:
        reader = csv.reader(file)
        inicio_sesion = datetime.utcfromtimestamp(float(next(reader)[0])).replace(tzinfo=utc)
        tasa_muestreo = float(next(reader)[0])
        datos = [float(row[0]) for row in reader]

    promedio = mean(datos)
    mediana = median(datos)
    maximo = max(datos)
    minimo = min(datos)

    # Diccionario para mapear nombres de tipo_dato a clases de modelo
    tipo_dato_to_model = {
        'temperatura': AnalisisTemperatura,
        'frecuenciacardiaca': AnalisisFrecuenciaCardiaca,
        'bvp': AnalisisBVP,
        'ibi': AnalisisIBI
    }

    # Seleccionar la clase de modelo correcta
    ModelClass = tipo_dato_to_model[tipo_dato]

    # Crear una instancia y guardar en la base de datos
    analisis = ModelClass.objects.create(
        usuario=usuario,
        promedio=promedio,
        mediana=mediana,
        maximo=maximo,
        minimo=minimo,
        inicio_sesion=inicio_sesion,
        tasa_muestreo=tasa_muestreo
    )
    os.remove(ruta_archivo)
    return {
        f'promedio_{tipo_dato}': promedio,
        f'mediana_{tipo_dato}': mediana,
        f'max_{tipo_dato}': maximo,
        f'min_{tipo_dato}': minimo
    }

def procesar_archivo_temp(archivo, fs, usuario):
    return procesar_archivo_generico(archivo, fs, usuario, 'temperatura')

def procesar_archivo_hr(archivo, fs, usuario):
    return procesar_archivo_generico(archivo, fs, usuario, 'frecuenciacardiaca')

def procesar_archivo_bvp(archivo, fs, usuario):
    return procesar_archivo_generico(archivo, fs, usuario, 'bvp')

def procesar_archivo_ibi(archivo, fs, usuario):
    return procesar_archivo_generico(archivo, fs, usuario, 'ibi')

def procesar_archivo_acc(archivo, fs, usuario):
    nombre_archivo_acc = fs.save(archivo.name, archivo)
    ruta_archivo_acc = fs.path(nombre_archivo_acc)
    x_vals, y_vals, z_vals = [], [], []

    with open(ruta_archivo_acc, 'r') as f:
        reader = csv.reader(f)
        inicio_sesion_acc = datetime.utcfromtimestamp(float(next(reader)[0])).replace(tzinfo=utc)
        tasa_muestreo_acc = float(next(reader)[0])
        for row in reader:
            x_vals.append(float(row[0]))
            y_vals.append(float(row[1]))
            z_vals.append(float(row[2]))

    promedio_x, promedio_y, promedio_z = mean(x_vals), mean(y_vals), mean(z_vals)
    mediana_x, mediana_y, mediana_z = median(x_vals), median(y_vals), median(z_vals)
    max_x, max_y, max_z = max(x_vals), max(y_vals), max(z_vals)
    min_x, min_y, min_z = min(x_vals), min(y_vals), min(z_vals)

    AnalisisAcelerometro.objects.create(
        usuario=usuario,
        promedio_x=promedio_x,
        promedio_y=promedio_y,
        promedio_z=promedio_z,
        mediana_x=mediana_x,
        mediana_y=mediana_y,
        mediana_z=mediana_z,
        maximo_x=max_x,
        maximo_y=max_y,
        maximo_z=max_z,
        minimo_x=min_x,
        minimo_y=min_y,
        minimo_z=min_z,
        inicio_sesion=inicio_sesion_acc,
        tasa_muestreo=tasa_muestreo_acc
    )
    os.remove(ruta_archivo_acc)
    return {
        'promedio_x': promedio_x,
        'promedio_y': promedio_y,
        'promedio_z': promedio_z,
        'mediana_x': mediana_x,
        'mediana_y': mediana_y,
        'mediana_z': mediana_z,
        'max_x': max_x,
        'max_y': max_y,
        'max_z': max_z,
        'min_x': min_x,
        'min_y': min_y,
        'min_z': min_z,
    }
