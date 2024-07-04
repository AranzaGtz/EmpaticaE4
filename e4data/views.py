import csv
import datetime
import os
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import AnalisisTemperatura, AnalisisFrecuenciaCardiaca, Usuario
from .forms import ArchivoForm
from statistics import mean, median

#    --   VISTAS GENERALES    --

# Vista para capturar los archivos
def captura_file(request):
     if request.method == 'POST':
          formulario = ArchivoForm(request.POST, request.FILES)
          if formulario.is_valid():
               fs = FileSystemStorage()
               contexto = {'form': formulario}

               nombre = formulario.cleaned_data['nombre']
               edad = formulario.cleaned_data['edad']
               usuario, created = Usuario.objects.get_or_create(nombre=nombre, edad=edad)

               # Procesar archivo TEMP.csv
               if 'archivo_temp' in request.FILES:
                    archivo_temp = request.FILES['archivo_temp']
                    nombre_archivo_temp = fs.save(archivo_temp.name, archivo_temp)
                    ruta_archivo_temp = fs.path(nombre_archivo_temp)

                    with open(ruta_archivo_temp, 'r') as f:
                         reader = csv.reader(f)
                         inicio_sesion_temp = datetime.datetime.utcfromtimestamp(float(next(reader)[0]))
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

                    contexto.update({
                         'promedio_temp': promedio_temp,
                         'mediana_temp': mediana_temp,
                         'max_temp': max_temp,
                         'min_temp': min_temp,
                         'resumen_temp': resumen,
                         'temperaturas': temperaturas
                    })
                    os.remove(ruta_archivo_temp)

               # Procesar archivo HR.csv
               if 'archivo_hr' in request.FILES:
                    archivo_hr = request.FILES['archivo_hr']
                    nombre_archivo_hr = fs.save(archivo_hr.name, archivo_hr)
                    ruta_archivo_hr = fs.path(nombre_archivo_hr)

                    with open(ruta_archivo_hr, 'r') as f:
                         reader = csv.reader(f)
                         inicio_sesion_hr = datetime.datetime.utcfromtimestamp(float(next(reader)[0]))
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

                    contexto.update({
                         'promedio_hr': promedio_hr,
                         'mediana_hr': mediana_hr,
                         'max_hr': max_hr,
                         'min_hr': min_hr,
                         'resumen_hr': resumen_hr,
                         'frecuencias': frecuencias
                    })
                    os.remove(ruta_archivo_hr)

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