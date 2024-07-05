from concurrent.futures import ThreadPoolExecutor
import csv
import datetime
import os
import pytz  # Importa pytz para manejar las zonas horarias
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .models import AnalisisAcelerometro, AnalisisTemperatura, AnalisisFrecuenciaCardiaca, Usuario
from .forms import ArchivoForm
from datetime import datetime
from statistics import mean, median

# Define la zona horaria UTC
utc = pytz.UTC

#    --   VISTAS GENERALES    --

def captura_file(request):
    if request.method == 'POST':
        # Redirigir a la página de carga
        return HttpResponseRedirect(reverse('loading'))
    else:
        formulario = ArchivoForm()
    return render(request, 'upload.html', {'form': formulario})

def loading_view(request):
    return render(request, 'loading.html')

# Vista para capturar los archivos
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

                    if 'archivo_temp' in request.FILES:
                         archivo_temp = request.FILES['archivo_temp']
                         futures.append(executor.submit(procesar_archivo_temp, archivo_temp, fs, usuario))

                    if 'archivo_hr' in request.FILES:
                         archivo_hr = request.FILES['archivo_hr']
                         futures.append(executor.submit(procesar_archivo_hr, archivo_hr, fs, usuario, edad))

                    if 'archivo_acc' in request.FILES:
                         archivo_acc = request.FILES['archivo_acc']
                         futures.append(executor.submit(procesar_archivo_acc, archivo_acc, fs, usuario))

                    for future in futures:
                         resultado = future.result()
                         contexto.update(resultado)

               return render(request, 'upload.html', contexto)
     else:
          formulario = ArchivoForm()
     return render(request, 'upload.html', {'form': formulario})

# Vista para resumen del analisis de temperatura
def resumen_analisis(temperaturas):
     bajas = sum(1 for t in temperaturas if clasificar_temperatura(t) == 'baja')
     altas = sum(1 for t in temperaturas if clasificar_temperatura(t) == 'alta')
     normales = sum(1 for t in temperaturas if clasificar_temperatura(t) == 'normal')
     errores = sum(1 for t in temperaturas if clasificar_temperatura(t) == 'error')

     total = len(temperaturas)
     resumen = "Resumen del análisis de temperatura:\n"
     if normales > 0:
          resumen += f" - {normales/total*100:.2f}% de las temperaturas son normales.\n"
     if bajas > 0:
          resumen += f" - {bajas/total*100:.2f}% de las temperaturas son bajas.\n"
     if altas > 0:
          resumen += f" - {altas/total*100:.2f}% de las temperaturas son altas.\n"
     if errores > 0:
          resumen += f" - {errores/total*100:.2f}% de las temperaturas parecen ser errores.\n"

     return resumen

# Vista para saber si el suseso estuvo realizado con exito
def archivo_suseso(request):
     return render(request, 'upload_success.html')

#    --   VISTAS TEMPERATURA    --

# Vista para procesar archivo temp.csv
def procesar_archivo_temp(archivo_temp, fs, usuario):
    nombre_archivo_temp = fs.save(archivo_temp.name, archivo_temp)
    ruta_archivo_temp = fs.path(nombre_archivo_temp)

    with open(ruta_archivo_temp, 'r') as f:
        reader = csv.reader(f)
        inicio_sesion_temp = datetime.utcfromtimestamp(float(next(reader)[0])).replace(tzinfo=utc)
        tasa_muestreo_temp = float(next(reader)[0])
        temperaturas = [float(row[0]) for row in reader]

    promedio_temp = mean(temperaturas)
    mediana_temp = median(temperaturas)
    max_temp = max(temperaturas)
    min_temp = min(temperaturas)
    resumen = f"Promedio de temperatura: {promedio_temp:.2f} °C, Mediana: {mediana_temp:.2f} °C, Máxima: {max_temp:.2f} °C, Mínima: {min_temp:.2f} °C"

    analisis = AnalisisTemperatura(
        usuario=usuario,
        promedio=promedio_temp,
        mediana=mediana_temp,
        maximo=max_temp,
        minimo=min_temp,
        inicio_sesion=inicio_sesion_temp,
        tasa_muestreo=tasa_muestreo_temp
    )
    analisis.save()
    os.remove(ruta_archivo_temp)

    return {
        'promedio_temp': promedio_temp,
        'mediana_temp': mediana_temp,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'resumen_temp': resumen,
        'temperaturas': temperaturas
    }

# Vista para clasificar la temperatura
def clasificar_temperatura(valor):
     if valor < 36.1:
          return 'baja'
     elif valor > 37.2:
          return 'alta'
     elif valor >= 36.1 and valor <= 37.2:
          return 'normal'
     else:
          return 'error'
    
#    --   VISTAS FRECUENCIA CARDIACA    --

# Vista para procesar rh.csv
def procesar_archivo_hr(archivo_hr, fs, usuario, edad):
    nombre_archivo_hr = fs.save(archivo_hr.name, archivo_hr)
    ruta_archivo_hr = fs.path(nombre_archivo_hr)

    with open(ruta_archivo_hr, 'r') as f:
        reader = csv.reader(f)
        inicio_sesion_hr = datetime.utcfromtimestamp(float(next(reader)[0])).replace(tzinfo=utc)
        tasa_muestreo_hr = float(next(reader)[0])
        frecuencias = [float(row[0]) for row in reader]

    promedio_hr = mean(frecuencias)
    mediana_hr = median(frecuencias)
    max_hr = max(frecuencias)
    min_hr = min(frecuencias)
    resumen_hr = resumen_analisis_frecuencia(frecuencias, edad)

    analisis_hr = AnalisisFrecuenciaCardiaca(
        usuario=usuario,
        promedio=promedio_hr,
        mediana=mediana_hr,
        maximo=max_hr,
        minimo=min_hr,
        inicio_sesion=inicio_sesion_hr,
        tasa_muestreo=tasa_muestreo_hr
    )
    analisis_hr.save()
    os.remove(ruta_archivo_hr)

    return {
        'promedio_hr': promedio_hr,
        'mediana_hr': mediana_hr,
        'max_hr': max_hr,
        'min_hr': min_hr,
        'resumen_hr': resumen_hr,
        'frecuencias': frecuencias
    }

# Función para clasificar la frecuencia cardíaca según los rangos de edad
def clasificar_frecuencia_cardiaca(valor, edad):
     if edad <= 1/12:  # Hasta 1 mes
          if valor < 70:
               return 'baja'
          elif valor > 190:
               return 'alta'
          else:
               return 'normal'
     elif edad <= 11/12:  # De 1 a 11 meses
          if valor < 80:
               return 'baja'
          elif valor > 160:
               return 'alta'
          else:
               return 'normal'
     elif edad <= 2:  # De 1 a 2 años
          if valor < 80:
               return 'baja'
          elif valor > 130:
               return 'alta'
          else:
               return 'normal'
     elif edad <= 4:  # De 3 a 4 años
          if valor < 80:
               return 'baja'
          elif valor > 120:
               return 'alta'
          else:
               return 'normal'
     elif edad <= 6:  # De 5 a 6 años
          if valor < 75:
               return 'baja'
          elif valor > 115:
               return 'alta'
          else:
               return 'normal'
     elif edad <= 9:  # De 7 a 9 años
          if valor < 70:
               return 'baja'
          elif valor > 110:
               return 'alta'
          else:
               return 'normal'
     else:  # Más de 10 años
          if valor < 60:
               return 'baja'
          elif valor > 100:
               return 'alta'
          else:
               return 'normal'

# Vista para resumen del analisis de temperatura
def resumen_analisis_frecuencia(frecuencias, edad):
     bajas = sum(1 for f in frecuencias if clasificar_frecuencia_cardiaca(f, edad) == 'baja')
     altas = sum(1 for f in frecuencias if clasificar_frecuencia_cardiaca(f, edad) == 'alta')
     normales = sum(1 for f in frecuencias if clasificar_frecuencia_cardiaca(f, edad) == 'normal')

     total = len(frecuencias)
     resumen = "Resumen del análisis de frecuencia cardíaca:\n"
     if normales > 0:
          resumen += f" - {normales/total*100:.2f}% de las frecuencias son normales.\n"
     if bajas > 0:
          resumen += f" - {bajas/total*100:.2f}% de las frecuencias son bajas.\n"
     if altas > 0:
          resumen += f" - {altas/total*100:.2f}% de las frecuencias son altas.\n"

     return resumen

#    -- VISTAS PARA ACELEROMETRO   --

# Vista para procesar archivo acc.csv
def procesar_archivo_acc(archivo_acc, fs, usuario):
    nombre_archivo_acc = fs.save(archivo_acc.name, archivo_acc)
    ruta_archivo_acc = fs.path(nombre_archivo_acc)

    x_vals = []
    y_vals = []
    z_vals = []

    with open(ruta_archivo_acc, 'r') as f:
        reader = csv.reader(f)
        inicio_sesion_acc = datetime.utcfromtimestamp(float(next(reader)[0])).replace(tzinfo=utc)
        tasa_muestreo_acc = float(next(reader)[0])
        for row in reader:
            x_vals.append(float(row[0]))
            y_vals.append(float(row[1]))
            z_vals.append(float(row[2]))

    promedio_x = mean(x_vals)
    promedio_y = mean(y_vals)
    promedio_z = mean(z_vals)
    mediana_x = median(x_vals)
    mediana_y = median(y_vals)
    mediana_z = median(z_vals)
    max_x = max(x_vals)
    max_y = max(y_vals)
    max_z = max(z_vals)
    min_x = min(x_vals)
    min_y = min(y_vals)
    min_z = min(z_vals)

    resumen_acc = resumen_analisis_acelerometro(x_vals, y_vals, z_vals)

    analisis_acc = AnalisisAcelerometro(
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
    analisis_acc.save()
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
        'resumen_acc': resumen_acc,
        'aceleracion_x': x_vals,
        'aceleracion_y': y_vals,
        'aceleracion_z': z_vals
    }

# Función para resumen del análisis del acelerómetro
def resumen_analisis_acelerometro(x_vals, y_vals, z_vals):
    def clasificar(valor):
          if valor < -1:
               return 'baja'
          elif valor > 1:
               return 'alta'
          else:
               return 'normal'

    resumen_x = f"Eje X - {sum(1 for x in x_vals if clasificar(x) == 'normal') / len(x_vals) * 100:.2f}% de los datos son normales. - {sum(1 for x in x_vals if clasificar(x) == 'baja') / len(x_vals) * 100:.2f}% de los datos son bajas. - {sum(1 for x in x_vals if clasificar(x) == 'alta') / len(x_vals) * 100:.2f}% de los datos son altas."
    resumen_y = f"Eje Y - {sum(1 for y in y_vals if clasificar(y) == 'normal') / len(y_vals) * 100:.2f}% de los datos son normales. - {sum(1 for y in y_vals if clasificar(y) == 'baja') / len(y_vals) * 100:.2f}% de los datos son bajas. - {sum(1 for y in y_vals if clasificar(y) == 'alta') / len(y_vals) * 100:.2f}% de los datos son altas."
    resumen_z = f"Eje Z - {sum(1 for z in z_vals if clasificar(z) == 'normal') / len(z_vals) * 100:.2f}% de los datos son normales. - {sum(1 for z in z_vals if clasificar(z) == 'baja') / len(z_vals) * 100:.2f}% de los datos son bajas. - {sum(1 for z in z_vals if clasificar(z) == 'alta') / len(z_vals) * 100:.2f}% de los datos son altas."

    return f"Resumen del análisis del acelerómetro: {resumen_x} {resumen_y} {resumen_z}"