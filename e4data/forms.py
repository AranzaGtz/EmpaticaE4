from django import forms

class ArchivoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    edad = forms.IntegerField(min_value=0, label='Edad')
    archivo_temp = forms.FileField(label='Archivo de Temperatura (TEMP.csv)')
    archivo_hr = forms.FileField(label='Archivo de Frecuencia Cardíaca (HR.csv)', required=False)
    archivo_acc = forms.FileField(label='Archivo de Acelerometro (ACC.csv)',required=False)
    # Necesitamos crear este formulario para permitir la carga de archivos CSV
    

class LoginForm(forms.Form):
    user = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, max_length=20)
