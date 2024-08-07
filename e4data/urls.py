from django.urls import path
from .views import captura_file, procesar_archivos, loading_view

urlpatterns = [
    path('', captura_file, name='captura_file'),
    path('procesar/', procesar_archivos, name='procesar_archivos'),
    path('loading/', loading_view, name='loading'),
]
