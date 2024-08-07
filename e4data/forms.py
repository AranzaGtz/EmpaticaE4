from django import forms

class ArchivoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    edad = forms.IntegerField(min_value=0, label='Edad')
    archivo_temp = forms.FileField(label='Archivo de Temperatura (TEMP.csv)', required=False)
    archivo_hr = forms.FileField(label='Archivo de Frecuencia Cardíaca (HR.csv)', required=False)
<<<<<<< HEAD
    archivo_acc = forms.FileField(label='Archivo de Acelerómetro (ACC.csv)', required=False)
    archivo_bvp = forms.FileField(label='Archivo de BVP (BVP.csv)', required=False)
    archivo_ibi = forms.FileField(label='Archivo de IBI (IBI.csv)', required=False)
    archivo_eda = forms.FileField(label='Archivo de EDA (EDA.csv)', required=False)  # Nuevo campo
=======
    archivo_acc = forms.FileField(label='Archivo de Acelerometro (ACC.csv)',required=False)
    # Necesitamos crear este formulario para permitir la carga de archivos CSV
    

class LoginForm(forms.Form):
    user = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, max_length=20)
>>>>>>> ada897e17210352c794746f926b1530fe4cee99a
