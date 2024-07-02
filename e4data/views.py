import csv
from datetime import timedelta
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import archivo_form

def captura_file(request):
    if request.method == 'POST':
        formulario = archivo_form(request.POST, request.FILES)
        if formulario.is_valid():
            archivo = request.FILES['archivo']
            fs = FileSystemStorage()
            nombre_archivo = fs.save(archivo.name, archivo)
            ruta_archivo = fs.path(nombre_archivo)
            
            with open(ruta_archivo, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Salta el encabezado
                for row in reader:
                    # Procesa cada fila del CSV
                    pass
            
            return redirect('upload_success')
    else:
        formulario = archivo_form()
    return render(request, 'upload.html', {'form': formulario})

def archivo_suseso(request):
    return render(request, 'upload_success.html')
