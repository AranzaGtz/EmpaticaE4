from django.urls import path
from . import views

urlpatterns = [
    
    #   URLS PARA TEMPERATURA
    path('', views.captura_file, name='index'),
    path('upload/success/', views.archivo_suseso, name='upload_success'),  # Verifica esta línea

    #   URLS PARA FRECUENCIA CARDIACA
    
    
]