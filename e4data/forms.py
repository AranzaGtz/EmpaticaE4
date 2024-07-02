from django import forms

class archivo_form(forms.Form):
    archivo = forms.FileField()
# Necesitamos crear este formulario para permitir la carga de archivos CSV