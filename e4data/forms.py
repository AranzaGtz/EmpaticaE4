from django import forms

class ArchivoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    edad = forms.IntegerField(min_value=0, label='Edad')
    archivo_temp = forms.FileField(label='Archivo de Temperatura (TEMP.csv)', required=False)
    archivo_hr = forms.FileField(label='Archivo de Frecuencia Cardíaca (HR.csv)', required=False)
    archivo_acc = forms.FileField(label='Archivo de Acelerómetro (ACC.csv)', required=False)
    archivo_bvp = forms.FileField(label='Archivo de BVP (BVP.csv)', required=False)
    archivo_ibi = forms.FileField(label='Archivo de IBI (IBI.csv)', required=False)
    archivo_eda = forms.FileField(label='Archivo de EDA (EDA.csv)', required=False)  # Nuevo campo
