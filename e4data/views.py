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
                     AnalisisBVP, AnalisisIBI, AnalisisEDA, Usuario)
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
                file_keys = ['temp', 'hr', 'acc', 'bvp', 'ibi', 'eda']
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
        'frecuenciaCardiaca': AnalisisFrecuenciaCardiaca,
        'bvp': AnalisisBVP,
        'ibi': AnalisisIBI,
        'eda': AnalisisEDA
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

    # Generar un resumen o diagnóstico específico
    resumen = generar_resumen(promedio, maximo, minimo, tipo_dato)

    return {
        f'promedio_{tipo_dato}': promedio,
        f'mediana_{tipo_dato}': mediana,
        f'max_{tipo_dato}': maximo,
        f'min_{tipo_dato}': minimo,
        f'resumen_{tipo_dato}': resumen,
        f'{tipo_dato}_data': datos  # Aquí estamos asegurando que los datos se pasen al template
    }

def procesar_archivo_temp(archivo, fs, usuario):
    return procesar_archivo_generico(archivo, fs, usuario, 'temperatura')

def procesar_archivo_hr(archivo, fs, usuario):
    return procesar_archivo_generico(archivo, fs, usuario, 'frecuenciaCardiaca')

def procesar_archivo_bvp(archivo, fs, usuario):
    return procesar_archivo_generico(archivo, fs, usuario, 'bvp')

def procesar_archivo_ibi(archivo, fs, usuario):
    return procesar_archivo_generico(archivo, fs, usuario, 'ibi')

def procesar_archivo_eda(archivo, fs, usuario):
    return procesar_archivo_generico(archivo, fs, usuario, 'eda')

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
    
    # Generar un resumen o diagnóstico específico para ACC
    resumen_acc = generar_resumen_acc(promedio_x, promedio_y, promedio_z)

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
        'resumen_acc': resumen_acc
    }

def generar_resumen(promedio, maximo, minimo, tipo_dato):
    if tipo_dato == 'eda':
        if promedio < 0.1:
            return "Tu nivel de actividad electrodermal es bajo, lo cual puede indicar baja respuesta emocional o estrés."
        elif promedio > 1.0:
            return "Tu nivel de actividad electrodermal es alto, lo cual puede indicar alta respuesta emocional o estrés."
        else:
            return "Tu nivel de actividad electrodermal está en un rango normal."
    elif tipo_dato == 'temperatura':
        if promedio < 36.1:
            return "Tu temperatura corporal promedio está por debajo de lo normal."
        elif promedio > 37.2:
            return "Tu temperatura corporal promedio está por encima de lo normal."
        else:
            return "Tu temperatura corporal está en un rango normal."
    elif tipo_dato == 'frecuenciaCardiaca':
        if promedio < 60:
            return "Tu frecuencia cardíaca es baja, podrías estar en reposo o en forma."
        elif promedio > 100:
            return "Tu frecuencia cardíaca es alta, podrías estar experimentando estrés o haciendo ejercicio."
        else:
            return "Tu frecuencia cardíaca está en un rango normal."
    elif tipo_dato == 'bvp':
        return "Análisis de BVP completo. Sin comentarios específicos."
    elif tipo_dato == 'ibi':
        if promedio < 600:
            return "Tu intervalo de latidos es corto, podrías estar en una situación de estrés o ejercicio."
        elif promedio > 1000:
            return "Tu intervalo de latidos es largo, podrías estar en reposo o muy relajado."
        else:
            return "Tu intervalo de latidos está en un rango normal."

def generar_resumen_acc(promedio_x, promedio_y, promedio_z):
    actividad_promedio = (abs(promedio_x) + abs(promedio_y) + abs(promedio_z)) / 3
    if actividad_promedio < 0.2:
        return "La actividad general es baja, indicando reposo o muy poca actividad."
    elif actividad_promedio > 1.0:
        return "La actividad general es alta, indicando movimiento o ejercicio intenso."
    else:
        return "La actividad general está en un rango normal, indicando actividad moderada."

