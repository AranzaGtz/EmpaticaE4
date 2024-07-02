import csv
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage # Para manejar la carga y almacenamiento de archivos.
from .forms import archivo_form
from statistics import mean, median # Para calcular estadísticas.

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

            contexto = {
                'promedio_temp': promedio_temp,
                'mediana_temp': mediana_temp,
                'max_temp': max_temp,
                'min_temp': min_temp,
                'temperaturas': temperaturas,
                'form': formulario
            }
            
            return render(request, 'upload.html', contexto)
    else:
        formulario = archivo_form()
    return render(request, 'upload.html', {'form': formulario})

# Vista para saber si el suseso estuvo realizado con exito
def archivo_suseso(request):
    return render(request, 'upload_success.html')
