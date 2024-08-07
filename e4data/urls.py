from django.urls import path
from .views import captura_file, procesar_archivos, loading_view

urlpatterns = [
<<<<<<< HEAD
    path('', captura_file, name='captura_file'),
    path('procesar/', procesar_archivos, name='procesar_archivos'),
    path('loading/', loading_view, name='loading'),
]
=======
    
    # path('', views.captura_file, name='index'),
    # path('upload/success/', views.archivo_suseso, name='upload_success'),  # Verifica esta línea
    path('', views.captura_file, name='captura_file'),
    path('procesar_archivos/', views.procesar_archivos, name='procesar_archivos'),
    path('loading/', views.loading_view, name='loading'),
    path('login/', views.login_view, name='login'),
    
]
>>>>>>> ada897e17210352c794746f926b1530fe4cee99a
