from django.urls import path
from . import views

urlpatterns = [
    path('', views.captura_file, name='index'),
    path('upload/success/', views.archivo_suseso, name='upload_success'),  # Verifica esta línea

]