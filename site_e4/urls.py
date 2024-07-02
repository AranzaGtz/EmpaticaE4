
from django.contrib import admin
from django.urls import path, include
from e4data import views  # Importa las vistas de tu aplicación

urlpatterns = [
    path('admin/', admin.site.urls),
    path('e4data/', include('e4data.urls')),
    path('', views.captura_file, name='home'),  # Redirigir la raíz a la vista de sesiones
]