import csv
import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage # Para manejar la carga y almacenamiento de archivos.
from django.conf import settings
from .models import AnalisisTemperatura
from .forms import archivo_form
from statistics import mean, median # Para calcular estadísticas.

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


# Vista para subir archivo
def captura_file(request):
    if request.method == 'POST':
        formulario = archivo_form(request.POST, request.FILES)
        if formulario.is_valid():
            archivo = request.FILES['archivo']
            fs = FileSystemStorage()
            nombre_archivo = fs.save(archivo.name, archivo)
            ruta_archivo = fs.path(nombre_archivo)
            
            temperaturas = []

            with open(ruta_archivo, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Saltar el encabezado
                for row in reader:
                    valor = float(row[0])
                    temperaturas.append(valor)
            
            # Calcular estadísticas
            promedio_temp = mean(temperaturas)
            mediana_temp = median(temperaturas)
            max_temp = max(temperaturas)
            min_temp = min(temperaturas)

            # Generar resumen del análisis
            resumen = resumen_analisis(temperaturas)

            # Guardar en la base de datos
            analisis = AnalisisTemperatura(
                promedio=promedio_temp,
                mediana=mediana_temp,
                maximo=max_temp,
                minimo=min_temp
            )
            analisis.save()

            # Borrar el archivo después de procesarlo
            os.remove(ruta_archivo)

            contexto = {
                'promedio_temp': promedio_temp,
                'mediana_temp': mediana_temp,
                'max_temp': max_temp,
                'min_temp': min_temp,
                'resumen': resumen,
                'form': formulario
            }
            
            return render(request, 'upload.html', contexto)
    else:
        formulario = archivo_form()
    return render(request, 'upload.html', {'form': formulario})

# Vista para saber si el suseso estuvo realizado con exito
def archivo_suseso(request):
    return render(request, 'upload_success.html')
