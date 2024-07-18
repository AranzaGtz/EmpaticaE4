from django.urls import path
from . import views

urlpatterns = [
    
    # path('', views.captura_file, name='index'),
    # path('upload/success/', views.archivo_suseso, name='upload_success'),  # Verifica esta línea
    path('', views.captura_file, name='captura_file'),
    path('procesar_archivos/', views.procesar_archivos, name='procesar_archivos'),
    path('loading/', views.loading_view, name='loading'),
    path('login/', views.login_view, name='login'),
    
]