from django import forms
from .models import Session

DATA_TYPE_CHOICES = [
    ('BVP', 'BVP'),
    ('EDA', 'EDA'),
    ('ACC', 'Acceleration'),
    ('HR', 'Heart Rate'),
    ('IBI', 'Inter-Beat Interval'),
    ('TEMP', 'Temperature'),
]

class UploadFileForm(forms.Form):
    session = forms.ModelChoiceField(queryset=Session.objects.all())
    data_type = forms.ChoiceField(choices=DATA_TYPE_CHOICES)
    file = forms.FileField()
# Necesitamos crear este formulario para permitir la carga de archivos CSV