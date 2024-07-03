from django.contrib import admin
from .models import AnalisisTemperatura, AnalisisFrecuenciaCardiaca, Usuario

# Register your models here.
admin.site.register(AnalisisTemperatura)
admin.site.register(AnalisisFrecuenciaCardiaca)
admin.site.register(Usuario)