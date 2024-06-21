import csv
from datetime import  timedelta
from django.http import HttpResponse
from django.shortcuts import render
from e4data.forms import UploadFileForm
from .models import Session, BVP, EDA, Acceleration, HR, IBI, TEMP

def handle_uploaded_file(file, session, data_type):
    decoded_file = file.read().decode('utf-8').splitlines()
    reader = csv.reader(decoded_file)
    start_time = session.start_time  # Obtener el tiempo de inicio de la sesión

    for index, row in enumerate(reader):
        timestamp = start_time + timedelta(seconds=index)  # Asumiendo que cada fila es un segundo
        if data_type == 'BVP':
            value = float(row[0])
            BVP.objects.create(session=session, timestamp=timestamp, value=value)
        elif data_type == 'EDA':
            value = float(row[0])
            EDA.objects.create(session=session, timestamp=timestamp, value=value)
        elif data_type == 'ACC':
            x, y, z = float(row[0]), float(row[1]), float(row[2])
            Acceleration.objects.create(session=session, timestamp=timestamp, x=x, y=y, z=z)
        elif data_type == 'HR':
            value = float(row[0])
            HR.objects.create(session=session, timestamp=timestamp, value=value)
        elif data_type == 'IBI':
            duration = float(row[0])
            IBI.objects.create(session=session, timestamp=timestamp, duration=duration)
        elif data_type == 'TEMP':
            value = float(row[0])
            TEMP.objects.create(session=session, timestamp=timestamp, value=value)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            session = form.cleaned_data['session']  # Asumiendo que el formulario tiene un campo de sesión
            data_type = form.cleaned_data['data_type']  # Campo para especificar el tipo de datos
            handle_uploaded_file(request.FILES['file'], session, data_type)
            return HttpResponse("File uploaded successfully")
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def session_list(request):
    sessions = Session.objects.all()
    return render(request, 'session_list.html', {'sessions': sessions})

def session_detail(request, session_id):
    session = Session.objects.get(id=session_id)
    bvp_data = BVP.objects.filter(session=session)
    eda_data = EDA.objects.filter(session=session)
    acc_data = Acceleration.objects.filter(session=session)
    hr_data = HR.objects.filter(session=session)
    ibi_data = IBI.objects.filter(session=session)
    temp_data = TEMP.objects.filter(session=session)
    return render(request, 'session_detail.html', {
        'session': session,
        'bvp_data': bvp_data,
        'eda_data': eda_data,
        'acc_data': acc_data,
        'hr_data': hr_data,
        'ibi_data': ibi_data,
        'temp_data': temp_data,
    })

